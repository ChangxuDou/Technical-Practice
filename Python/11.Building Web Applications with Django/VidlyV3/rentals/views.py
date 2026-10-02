import uuid
from decimal import Decimal, InvalidOperation
from datetime import timedelta
from functools import wraps
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.db.models import Q,Sum,Count,F
from django.db.models.functions import TruncDay,TruncMonth,TruncYear
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET
from movies.models import Movie,Genre
from .models import Customer,Rental,ReturnRecord,RentalItem,Coupon,CustomerCoupon,Ledger
from .forms import SignupForm,CustomerForm,MovieForm
from .services import checkout,settle,adjust_balance,BusinessError,is_staff,is_manager,authorize

def staff_only(fn):
    @login_required
    @wraps(fn)
    def wrapped(request,*a,**kw):
        if not is_staff(request.user):raise PermissionDenied
        return fn(request,*a,**kw)
    return wrapped

def manager_only(fn):
    @staff_only
    @wraps(fn)
    def wrapped(request,*a,**kw):
        if not is_manager(request.user):raise PermissionDenied
        return fn(request,*a,**kw)
    return wrapped

def home(request):
    films=Movie.objects.filter(active=True).select_related('genre')
    featured=films.filter(title='Interstellar').first() or films.first()
    return render(request,'home.html',{'featured':featured,'movies':films[:8],'film_count':films.count(),'genres':Genre.objects.annotate(count=Count('movie',filter=Q(movie__active=True))).filter(count__gt=0)})

def catalog(request):
    films=Movie.objects.filter(active=True).select_related('genre')
    q=request.GET.get('q','').strip();genre=request.GET.get('genre','')
    if q:films=films.filter(Q(title__icontains=q)|Q(director__icontains=q)|Q(barcode=q))
    if genre.isdigit():films=films.filter(genre_id=int(genre))
    if request.GET.get('available'):films=films.filter(number_in_stock__gt=0)
    sort=request.GET.get('sort','title')
    films=films.order_by({'title':'title','year':'-release_year','price':'daily_rate'}.get(sort,'title'))
    page=Paginator(films,12).get_page(request.GET.get('page'))
    params=request.GET.copy();params.pop('page',None)
    return render(request,'catalog.html',{'page':page,'genres':Genre.objects.all(),'q':q,'selected_genre':genre,'sort':sort,'query_string':params.urlencode()})

def detail(request,pk):
    movie=get_object_or_404(Movie.objects.select_related('genre'),pk=pk,active=True)
    return render(request,'detail.html',{'movie':movie,'related':Movie.objects.filter(active=True,genre=movie.genre).exclude(pk=pk)[:4]})

@require_POST
def bag_add(request,pk):
    movie=get_object_or_404(Movie,pk=pk,active=True)
    cart=request.session.get('cart',{}).copy();qty=cart.get(str(pk),0)+1
    if qty>min(movie.number_in_stock,20):messages.error(request,'Insufficient stock to add another copy.')
    else:
        cart[str(pk)]=qty;request.session['cart']=cart;messages.success(request,f'{movie.title} added to your rental bag.')
    return redirect('bag')

@require_POST
def bag_update(request,pk):
    cart=request.session.get('cart',{}).copy()
    try:qty=int(request.POST.get('quantity',0))
    except ValueError:qty=-1
    movie=get_object_or_404(Movie,pk=pk)
    if qty<0 or qty>20 or qty>movie.number_in_stock:messages.error(request,'The quantity is invalid or exceeds available stock.')
    elif qty==0:cart.pop(str(pk),None)
    else:cart[str(pk)]=qty
    request.session['cart']=cart
    return redirect('bag')

def bag(request):
    cart=request.session.get('cart',{});rows=[];total=Decimal('0')
    for movie in Movie.objects.filter(pk__in=cart).select_related('genre'):
        qty=cart[str(movie.pk)];subtotal=movie.daily_rate*qty;total+=subtotal
        rows.append({'movie':movie,'quantity':qty,'subtotal':subtotal})
    return render(request,'bag.html',{'rows':rows,'total':total,'request_key':uuid.uuid4()})

@login_required
@require_POST
def place_order(request):
    try:
        key=uuid.UUID(request.POST.get('request_key',''));days=int(request.POST.get('days','7'))
        customer=get_object_or_404(Customer,user=request.user)
        order=checkout(request.user,customer.pk,request.session.get('cart',{}),days,key)
        request.session['cart']={};messages.success(request,'Rental confirmed! Actual rental time will be charged on return.')
        return redirect('rental_detail',pk=order.pk)
    except (ValueError,BusinessError) as e:messages.error(request,str(e) if isinstance(e,BusinessError) else 'Invalid submission. Please try again.')
    return redirect('bag')

def signup(request):
    if request.user.is_authenticated:return redirect('my_rentals')
    form=SignupForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        try:
            with transaction.atomic():
                user=form.save();Customer.objects.create(user=user,full_name=form.cleaned_data['full_name'],phone=form.cleaned_data['phone'],email=form.cleaned_data['email'])
            login(request,user);messages.success(request,'Welcome to Vidly. You can now start renting movies.');return redirect('bag')
        except IntegrityError:form.add_error(None,'This username or phone number is already in use.')
    return render(request,'form.html',{'form':form,'title':'Your next chapter starts here.','eyebrow':'JOIN THE CLUB','submit':'Create account','intro':'Make room for your next favourite story.'})

@login_required
def my_rentals(request):
    customer=Customer.objects.filter(user=request.user).first()
    orders=Rental.objects.filter(customer=customer).prefetch_related('items__movie') if customer else Rental.objects.none()
    return render(request,'rentals.html',{'orders':orders,'customer':customer})

@login_required
def rental_detail(request,pk):
    order=get_object_or_404(Rental.objects.select_related('customer'),pk=pk);authorize(request.user,order.customer)
    error=''
    if request.method=='POST':
        if not is_staff(request.user):raise PermissionDenied
        try:
            key=uuid.UUID(request.POST.get('request_key',''))
            selected={i.pk:(int(request.POST.get(f'return_{i.pk}',0)),int(request.POST.get(f'lost_{i.pk}',0))) for i in order.items.all()}
            receipt=settle(request.user,order.pk,selected,request.POST.get('coupon') or None,request.POST.get('payment','cash'),key)
            messages.success(request,f'Return recorded. Settlement total: €{receipt.amount}.');return redirect('rental_detail',pk=pk)
        except (ValueError,BusinessError) as e:error=str(e) if isinstance(e,BusinessError) else 'Enter valid whole-number quantities.'
    coupons=order.customer.coupons.filter(used_at__isnull=True,coupon__active=True).filter(Q(coupon__expires_at__isnull=True)|Q(coupon__expires_at__gte=timezone.now())).select_related('coupon')
    return render(request,'rental_detail.html',{'order':order,'items':order.items.select_related('movie'),'receipts':order.returns.prefetch_related('items__rental_item'),'coupons':coupons,'request_key':uuid.uuid4(),'error':error})

@login_required
@require_POST
def claim_coupon(request):
    customer=get_object_or_404(Customer,user=request.user)
    coupon=Coupon.objects.filter(code=request.POST.get('code','').strip().upper(),active=True).filter(Q(expires_at__isnull=True)|Q(expires_at__gte=timezone.now())).first()
    if not coupon:messages.error(request,'This coupon code does not exist or has expired.')
    else:
        _,created=CustomerCoupon.objects.get_or_create(customer=customer,coupon=coupon)
        messages.success(request,'Coupon claimed. You can use it when returning your rental.' if created else 'You have already claimed this coupon.')
    return redirect('my_rentals')

@staff_only
def desk(request):
    orders=Rental.objects.filter(items__quantity__gt=F('items__returned_quantity')+F('items__lost_quantity')).distinct().select_related('customer').prefetch_related('items')
    return render(request,'desk.html',{'orders':orders,'customer_count':Customer.objects.count(),'stock':Movie.objects.aggregate(n=Sum('number_in_stock'))['n'] or 0,'today_revenue':ReturnRecord.objects.filter(created_at__date=timezone.localdate()).aggregate(n=Sum('amount'))['n'] or 0})

@staff_only
def customers(request):
    q=request.GET.get('q','').strip()
    rows=Customer.objects.filter(Q(phone__icontains=q)|Q(full_name__icontains=q)).order_by('full_name')
    return render(request,'customers.html',{'customers':rows,'q':q})

@staff_only
def customer_edit(request,pk=None):
    customer=get_object_or_404(Customer,pk=pk) if pk else None
    form=CustomerForm(request.POST or None,instance=customer)
    if request.method=='POST' and form.is_valid():
        form.save();messages.success(request,'Customer details saved.');return redirect('customers')
    return render(request,'form.html',{'form':form,'title':'Edit customer' if pk else 'Register customer','eyebrow':'CUSTOMERS','submit':'Save customer'})

@staff_only
def counter(request):
    error='';selected=request.POST.get('customer') or request.GET.get('customer','')
    if request.method=='POST':
        try:
            cart={}
            for line in request.POST.get('barcodes','').splitlines():
                if not line.strip():continue
                parts=line.strip().split();barcode=parts[0];qty=int(parts[1]) if len(parts)>1 else 1
                if qty<1:raise BusinessError('The quantity after the barcode must be greater than 0.')
                movie=Movie.objects.filter(barcode=barcode,active=True).first()
                if not movie:raise BusinessError(f'No listed movie was found for barcode {barcode} .')
                cart[movie.pk]=cart.get(movie.pk,0)+qty
            customer=get_object_or_404(Customer,pk=selected)
            order=checkout(request.user,customer.pk,cart,int(request.POST.get('days','7')),uuid.UUID(request.POST.get('request_key','')))
            messages.success(request,'Counter rental recorded.');return redirect('rental_detail',pk=order.pk)
        except (ValueError,BusinessError) as e:error=str(e) if isinstance(e,BusinessError) else 'Check the customer, quantities and rental period.'
    return render(request,'counter.html',{'customers':Customer.objects.filter(active=True),'movies':Movie.objects.filter(active=True),'selected':str(selected),'request_key':uuid.uuid4(),'error':error})

@staff_only
def wallet(request,pk):
    customer=get_object_or_404(Customer,pk=pk);error=''
    if request.method=='POST':
        try:
            amount=Decimal(request.POST.get('amount',''))
            if not amount.is_finite() or amount.as_tuple().exponent < -2:raise BusinessError('Amounts can have up to two decimal places.')
            adjust_balance(request.user,pk,amount,request.POST.get('kind'),uuid.UUID(request.POST.get('request_key','')))
            messages.success(request,'Wallet transaction recorded (simulation).');return redirect('wallet',pk=pk)
        except (InvalidOperation,ValueError,BusinessError) as e:error=str(e) if isinstance(e,BusinessError) else 'Invalid amount format.'
    return render(request,'wallet.html',{'customer':customer,'entries':customer.ledger.all().order_by('-created_at'),'request_key':uuid.uuid4(),'error':error})

@manager_only
def inventory(request):
    return render(request,'inventory.html',{'movies':Movie.objects.select_related('genre').all()})

@manager_only
def movie_edit(request,pk=None):
    # Lock the row while validating total stock against outstanding rentals.
    with transaction.atomic():
        movie=get_object_or_404(Movie.objects.select_for_update(),pk=pk) if pk else None
        outstanding=(movie.total_quantity-movie.number_in_stock) if movie else 0
        form=MovieForm(request.POST or None,instance=movie)
        if request.method=='POST' and form.is_valid():
            saved=form.save(commit=False)
            if saved.total_quantity<outstanding:form.add_error('total_quantity',f'There are {outstanding} copies still on loan. Total stock cannot be lower than this.')
            else:
                saved.number_in_stock=saved.total_quantity-outstanding;saved.save();messages.success(request,'Movie and stock saved.');return redirect('inventory')
    return render(request,'form.html',{'form':form,'title':'Edit movie' if pk else 'Add movie','eyebrow':'INVENTORY','submit':'Save movie','intro':'Changing total stock also changes available stock. Unlist movies with rental history to keep their records.'})

@manager_only
@require_POST
def movie_delete(request,pk):
    with transaction.atomic():
        movie=get_object_or_404(Movie.objects.select_for_update(),pk=pk)
        if movie.rental_items.exists() or movie.purchases.exists() or movie.moviewish_set.exists():movie.active=False;movie.save(update_fields=['active']);messages.success(request,'Movie unlisted. Historical records have been preserved.')
        else:movie.delete();messages.success(request,'Movie deleted.')
    return redirect('inventory')

@manager_only
def reports(request):
    period=request.GET.get('period','day')
    trunc={'day':TruncDay,'month':TruncMonth,'year':TruncYear}.get(period,TruncDay)
    revenue=ReturnRecord.objects.annotate(bucket=trunc('created_at')).values('bucket').annotate(total=Sum('amount'),count=Count('id')).order_by('-bucket')[:30]
    top_movies=RentalItem.objects.values('movie__title').annotate(total=Sum('quantity')).order_by('-total')[:10]
    top_customers=ReturnRecord.objects.values('rental__customer__full_name','rental__customer_id').annotate(total=Sum('amount')).order_by('-total')[:10]
    return render(request,'reports.html',{'revenue':revenue,'top_movies':top_movies,'top_customers':top_customers,'period':period,'total_revenue':ReturnRecord.objects.aggregate(n=Sum('amount'))['n'] or 0,'order_count':Rental.objects.count()})

@require_GET
def movie_api(request):
    data=list(Movie.objects.filter(active=True).values('id','title','release_year','number_in_stock','daily_rate','genre__name'))
    return JsonResponse({'meta':{'total_count':len(data)},'objects':data},json_dumps_params={'ensure_ascii':False})
