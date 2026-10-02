import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models import Q,F
from django.utils import timezone
from movies.models import Movie

class Customer(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,null=True,blank=True,related_name='customer')
    full_name=models.CharField('Full name',max_length=100)
    phone=models.CharField('Phone',max_length=30,unique=True)
    email=models.EmailField('Email',blank=True)
    active=models.BooleanField('Active',default=True)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    points=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(default=timezone.now)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(balance__gte=0),name='nonnegative_balance')]
    def __str__(self):return f'{self.full_name} · {self.phone}'

class Rental(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='rentals')
    operator=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    created_at=models.DateTimeField(default=timezone.now)
    due_at=models.DateTimeField()
    note=models.CharField(max_length=255,blank=True)
    request_key=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    class Meta: ordering=['-created_at']
    @property
    def closed(self):return not self.items.filter(quantity__gt=F('returned_quantity')+F('lost_quantity')).exists()
    @property
    def overdue(self):return not self.closed and timezone.now()>self.due_at
    @property
    def number(self):return f'VL{self.pk:06d}'

class RentalItem(models.Model):
    rental=models.ForeignKey(Rental,on_delete=models.PROTECT,related_name='items')
    movie=models.ForeignKey(Movie,on_delete=models.PROTECT,related_name='rental_items')
    title=models.CharField(max_length=255)
    quantity=models.PositiveIntegerField()
    daily_rate=models.DecimalField(max_digits=6,decimal_places=2)
    returned_quantity=models.PositiveIntegerField(default=0)
    lost_quantity=models.PositiveIntegerField(default=0)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(quantity__gt=0),name='positive_rental_quantity'),models.CheckConstraint(condition=Q(quantity__gte=F('returned_quantity')+F('lost_quantity')),name='settled_not_above_rented')]
    @property
    def remaining(self):return self.quantity-self.returned_quantity-self.lost_quantity

class Coupon(models.Model):
    code=models.CharField('Coupon code',max_length=30,unique=True)
    name=models.CharField('Name',max_length=100)
    percent=models.PositiveIntegerField('Rental discount (%)',default=10)
    active=models.BooleanField('Active',default=True)
    expires_at=models.DateTimeField('Expires at',null=True,blank=True)
    class Meta:
        constraints=[models.CheckConstraint(condition=Q(percent__gte=1)&Q(percent__lte=100),name='valid_discount_percent')]
    def __str__(self):return self.code

class CustomerCoupon(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='coupons')
    coupon=models.ForeignKey(Coupon,on_delete=models.PROTECT)
    claimed_at=models.DateTimeField(default=timezone.now)
    used_at=models.DateTimeField(null=True,blank=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['customer','coupon'],name='one_coupon_per_customer')]

class ReturnRecord(models.Model):
    rental=models.ForeignKey(Rental,on_delete=models.PROTECT,related_name='returns')
    operator=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    created_at=models.DateTimeField(default=timezone.now)
    rental_charge=models.DecimalField(max_digits=10,decimal_places=2)
    lost_charge=models.DecimalField(max_digits=10,decimal_places=2)
    discount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    coupon=models.OneToOneField(CustomerCoupon,on_delete=models.PROTECT,null=True,blank=True)
    payment_method=models.CharField(max_length=10,choices=[('cash','Simulated cash'),('balance','Balance')])
    request_key=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    class Meta: ordering=['-created_at']

class ReturnItem(models.Model):
    record=models.ForeignKey(ReturnRecord,on_delete=models.PROTECT,related_name='items')
    rental_item=models.ForeignKey(RentalItem,on_delete=models.PROTECT)
    quantity=models.PositiveIntegerField(default=0)
    lost_quantity=models.PositiveIntegerField(default=0)
    days=models.PositiveIntegerField()
    charged_amount=models.DecimalField(max_digits=10,decimal_places=2)

class Ledger(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='ledger')
    operator=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    kind=models.CharField(max_length=12,choices=[('recharge','Simulated top-up'),('refund','Balance refund'),('rental','Rental payment')])
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    balance_after=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(default=timezone.now)
    note=models.CharField(max_length=255,blank=True)
    request_key=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)


class RewardPolicy(models.Model):
    """Single store-wide policy; orders snapshot the rate before payment."""
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    money_unit = models.DecimalField('For every EUR', max_digits=8, decimal_places=2, default=1)
    points_unit = models.PositiveIntegerField('Award this many points', default=10)
    enabled = models.BooleanField('Enable customer simulated top-ups', default=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(id=1), name='singleton_reward_policy'),
            models.CheckConstraint(condition=Q(money_unit__gte=Decimal('0.01')) & Q(money_unit__lte=10000), name='reward_money_range'),
            models.CheckConstraint(condition=Q(points_unit__gte=1) & Q(points_unit__lte=10000), name='reward_points_range'),
        ]

    def __str__(self):
        return 'Top-up rewards policy'


class PolicyRevision(models.Model):
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    before = models.JSONField(default=dict)
    after = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)


class TopUp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_key = models.UUIDField(unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='topups')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    money_unit = models.DecimalField(max_digits=8, decimal_places=2)
    points_unit = models.PositiveIntegerField()
    awarded_points = models.PositiveIntegerField()
    status = models.CharField(max_length=12, default='pending', choices=[('pending','Pending payment'),('success','Payment successful'),('failed','Payment failed'),('cancelled','Cancelled'),('expired','Expired')])
    provider_reference = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    refunded_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reversed_points = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        constraints = [models.CheckConstraint(condition=Q(amount__gte=1) & Q(amount__lte=10000), name='topup_amount_range'), models.CheckConstraint(condition=Q(refunded_amount__lte=F('amount')), name='topup_refund_cap')]


class PointsEntry(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='points_entries')
    ledger = models.OneToOneField(Ledger, on_delete=models.PROTECT)
    delta = models.IntegerField()
    points_after = models.PositiveIntegerField()
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']


class MovieWish(models.Model):
    title = models.CharField('Requested movie', max_length=255)
    release_year = models.PositiveIntegerField('Release year')
    normalized_key = models.CharField(max_length=64, unique=True, editable=False)
    status = models.CharField(max_length=12, default='requested', choices=[('requested','Under review'),('planned','On order'),('available','Arrived'),('declined','Not planned')])
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True, blank=True)
    manager_note = models.CharField('Manager update', max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} ({self.release_year})'


class WishRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='wishes')
    wish = models.ForeignKey(MovieWish, on_delete=models.PROTECT, related_name='requests')
    note = models.CharField('Additional information', max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['customer','wish'], name='one_wish_per_customer')]
        ordering = ['-created_at']


class PurchaseOrder(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='purchases')
    wish = models.ForeignKey(MovieWish, on_delete=models.PROTECT, null=True, blank=True, related_name='purchases')
    quantity = models.PositiveIntegerField()
    received_quantity = models.PositiveIntegerField(default=0)
    supplier = models.CharField(max_length=120, blank=True)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    request_key = models.UUIDField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        constraints = [models.CheckConstraint(condition=Q(quantity__gt=0) & Q(received_quantity__lte=F('quantity')), name='purchase_quantity_range'), models.CheckConstraint(condition=Q(unit_cost__gte=0),name='purchase_cost_nonnegative')]

    @property
    def remaining(self):
        return self.quantity - self.received_quantity

    @property
    def status_label(self):
        return 'Fully received' if self.remaining == 0 else ('Partially received' if self.received_quantity else 'Awaiting delivery')

    @property
    def number(self):
        return f'PO{self.pk:06d}'


class StockReceipt(models.Model):
    purchase = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='receipts')
    quantity = models.PositiveIntegerField()
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    request_key = models.UUIDField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True)
