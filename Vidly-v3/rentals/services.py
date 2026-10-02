"""All stock and monetary changes go through these atomic services."""
import math
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .models import Customer,Rental,RentalItem,Coupon,CustomerCoupon,ReturnRecord,ReturnItem,Ledger
from movies.models import Movie

class BusinessError(Exception):pass

def is_manager(user):return user.is_authenticated and (user.is_superuser or (user.is_staff and user.groups.filter(name='Manager').exists()))
def is_staff(user):return user.is_authenticated and (is_manager(user) or (user.is_staff and user.groups.filter(name='Cashier').exists()))
def authorize(user,customer):
    if not user.is_authenticated or not (is_staff(user) or customer.user_id==user.pk): raise PermissionDenied

def money(x):return Decimal(x).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)

@transaction.atomic
def checkout(user,customer_id,cart,days,key):
    customer=Customer.objects.select_for_update().get(pk=customer_id)
    authorize(user,customer)
    existing=Rental.objects.filter(request_key=key).first()
    if existing:
        if existing.customer_id!=customer.pk:raise PermissionDenied
        return existing
    if not customer.active:raise BusinessError('This customer is inactive and cannot rent movies.')
    if not cart or not 1<=days<=30:raise BusinessError('Choose at least one movie and an estimated rental period of 1–30 days.')
    rental=Rental.objects.create(customer=customer,operator=user,due_at=timezone.now()+timedelta(days=days),request_key=key)
    for mid,qty in sorted(cart.items(),key=lambda x:int(x[0])):
        if not isinstance(qty,int) or not 1<=qty<=20:raise BusinessError('Choose between 1 and 20 copies of each movie.')
        movie=Movie.objects.select_for_update().filter(pk=mid).first()
        if movie is None:raise BusinessError('A movie in your rental bag has been removed. Please choose again.')
        updated=Movie.objects.filter(pk=mid,active=True,number_in_stock__gte=qty).update(number_in_stock=F('number_in_stock')-qty)
        if not updated:raise BusinessError(f'{movie.title} is unavailable or has insufficient stock. Please update your bag.')
        RentalItem.objects.create(rental=rental,movie=movie,title=movie.title,quantity=qty,daily_rate=movie.daily_rate)
    return rental

@transaction.atomic
def settle(user,rental_id,selections,coupon_id,method,key):
    if not is_staff(user):raise PermissionDenied
    rental=Rental.objects.select_for_update().select_related('customer').get(pk=rental_id)
    authorize(user,rental.customer)
    existing=ReturnRecord.objects.filter(request_key=key).first()
    if existing:
        if existing.rental_id!=rental.pk:raise PermissionDenied
        return existing
    if method not in ('cash','balance'):raise BusinessError('Choose a payment method.')
    customer=Customer.objects.select_for_update().get(pk=rental.customer_id)
    now=timezone.now();days=max(1,math.ceil((now-rental.created_at).total_seconds()/86400))
    rows=[];rent=Decimal('0');lost=Decimal('0')
    for item in rental.items.select_for_update().order_by('id'):
        normal,missing=selections.get(item.pk,(0,0))
        if normal<0 or missing<0 or normal+missing>item.remaining:raise BusinessError(f'{item.title}: the returned and lost quantities exceed the outstanding quantity.')
        if normal+missing:
            charge=money(item.daily_rate*days*normal)
            penalty=money(item.daily_rate*5*missing)
            rows.append((item,normal,missing,charge+penalty))
            rent+=charge;lost+=penalty
    if not rows:raise BusinessError('Select at least one copy to return or report as lost.')
    coupon=None;discount=Decimal('0')
    if coupon_id:
        coupon=CustomerCoupon.objects.select_for_update().select_related('coupon').filter(pk=coupon_id,customer=customer,used_at__isnull=True).first()
        if not coupon or not coupon.coupon.active or (coupon.coupon.expires_at and coupon.coupon.expires_at<now):raise BusinessError('This coupon is invalid, used or expired.')
        if rent<=0:raise BusinessError('Coupons apply to rental fees only, not lost-disc charges.')
        discount=money(rent*coupon.coupon.percent/100)
    amount=money(rent+lost-discount)
    if method=='balance':
        if customer.balance<amount:raise BusinessError('Insufficient balance. Top up your wallet or choose simulated cash.')
        customer.balance-=amount
    customer.save(update_fields=['balance'])
    record=ReturnRecord.objects.create(rental=rental,operator=user,rental_charge=rent,lost_charge=lost,discount=discount,amount=amount,coupon=coupon,payment_method=method,request_key=key)
    for item,normal,missing,charge in rows:
        item.returned_quantity+=normal;item.lost_quantity+=missing;item.save(update_fields=['returned_quantity','lost_quantity'])
        Movie.objects.filter(pk=item.movie_id).update(number_in_stock=F('number_in_stock')+normal,total_quantity=F('total_quantity')-missing)
        ReturnItem.objects.create(record=record,rental_item=item,quantity=normal,lost_quantity=missing,days=days,charged_amount=charge)
    if coupon:coupon.used_at=now;coupon.save(update_fields=['used_at'])
    if method=='balance':Ledger.objects.create(customer=customer,operator=user,kind='rental',amount=-amount,balance_after=customer.balance,request_key=key,note=f'{rental.number} Return settlement')
    return record

@transaction.atomic
def adjust_balance(user,customer_id,amount,kind,key):
    if not is_staff(user):raise PermissionDenied
    customer=Customer.objects.select_for_update().get(pk=customer_id)
    existing=Ledger.objects.filter(request_key=key).first()
    if existing:
        if existing.customer_id!=customer.pk:raise PermissionDenied
        return existing
    amount=money(amount)
    if amount<=0 or amount>10000 or kind not in ('recharge','refund'):raise BusinessError('The amount must be greater than 0 and no more than 10,000.')
    if kind=='refund':amount=-amount
    if customer.balance+amount<0:raise BusinessError('The refund cannot exceed the current balance.')
    customer.balance+=amount;customer.save(update_fields=['balance'])
    entry=Ledger.objects.create(customer=customer,operator=user,kind=kind,amount=amount,balance_after=customer.balance,request_key=key)
    if kind=='refund':
        from .workflows import reverse_refund_points
        reverse_refund_points(customer, -amount, entry)
    return entry
