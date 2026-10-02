import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Customer, MovieWish, WishRequest, RewardPolicy, TopUp, PurchaseOrder, PolicyRevision
from .forms import WishForm, TopUpForm, RewardPolicyForm, PurchaseForm
from .services import BusinessError, is_manager
from .views import manager_only, staff_only
from .workflows import (submit_wish, decline_wish, start_topup, finish_topup,
                        create_purchase, receive_purchase, configure_rewards)


def error_text(error):
    if isinstance(error, ValidationError):
        return '；'.join(error.messages)
    if isinstance(error, IntegrityError):
        return 'Duplicate record. Check the barcode or reopen the page.'
    if isinstance(error, ValueError):
        return 'Invalid submission. Check the details and try again.'
    return str(error)


@login_required
def wishlist(request):
    customer = get_object_or_404(Customer, user=request.user)
    form = WishForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            _, created = submit_wish(request.user, **form.cleaned_data)
            messages.success(request, 'Wish submitted. The manager can now see this request in the demand summary.' if created else 'You have already requested this movie. It will only count once.')
            return redirect('wishlist')
        except BusinessError as error:
            form.add_error(None, str(error))
    wishes = customer.wishes.select_related('wish__movie').annotate(supporters=Count('wish__requests'))
    return render(request, 'wishlist.html', {'form':form, 'wishes':wishes})


@manager_only
def wish_summary(request):
    rows = MovieWish.objects.annotate(supporters=Count('requests')).select_related('movie').order_by('-supporters','created_at')
    return render(request, 'wish_summary.html', {'wishes':rows})


@manager_only
def wish_review(request, pk):
    wish = get_object_or_404(MovieWish, pk=pk)
    if request.method == 'POST':
        try:
            decline_wish(request.user, pk, request.POST.get('note',''))
            messages.success(request, 'The update is now visible to the customer.')
            return redirect('wish_summary')
        except BusinessError as error:
            messages.error(request, str(error))
    return render(request, 'wish_review.html', {'wish':wish, 'requests':wish.requests.select_related('customer')})


@login_required
def my_wallet(request):
    customer = get_object_or_404(Customer, user=request.user)
    policy, _ = RewardPolicy.objects.get_or_create(pk=1)
    form = TopUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            order = start_topup(request.user, form.cleaned_data['amount'], uuid.UUID(request.POST.get('request_key','')))
            return redirect('mock_payment', order_id=order.pk)
        except (BusinessError, ValueError) as error:
            form.add_error(None, error_text(error))
    return render(request, 'my_wallet.html', {'customer':customer, 'policy':policy, 'form':form,
        'request_key':uuid.uuid4(), 'topups':customer.topups.all()[:30],
        'entries':customer.ledger.order_by('-created_at')[:30], 'points_entries':customer.points_entries.all()[:30]})


@login_required
def mock_payment(request, order_id):
    order = get_object_or_404(TopUp, pk=order_id)
    if order.customer.user_id != request.user.pk:
        raise PermissionDenied
    error = ''
    if request.method == 'POST':
        try:
            result = finish_topup(request.user, order_id, request.POST.get('outcome'))
            messages.success(request, f'Simulated payment result: {result.get_status_display()}.')
            return redirect('mock_payment', order_id=order_id)
        except BusinessError as exc:
            error = str(exc)
    return render(request, 'mock_payment.html', {'order':order, 'error':error})


@manager_only
def reward_settings(request):
    policy, _ = RewardPolicy.objects.get_or_create(pk=1)
    form = RewardPolicyForm(request.POST or None, instance=policy)
    if request.method == 'POST' and form.is_valid():
        configure_rewards(request.user, **form.cleaned_data)
        messages.success(request, 'Rewards policy saved. It applies only to top-up orders created from now on.')
        return redirect('reward_settings')
    return render(request, 'reward_settings.html', {'form':form, 'revisions':PolicyRevision.objects.select_related('operator').order_by('-created_at')[:20]})


@staff_only
def purchases(request):
    orders = PurchaseOrder.objects.select_related('movie','wish','operator')
    return render(request, 'purchases.html', {'orders':orders})


@manager_only
def purchase_new(request):
    initial = {'wish':request.GET.get('wish'), 'movie':request.GET.get('movie')}
    if request.GET.get('wish', '').isdigit():
        linked = MovieWish.objects.filter(pk=request.GET['wish']).first()
        if linked:
            initial.update(title=linked.title, release_year=linked.release_year, movie=linked.movie_id)
    form = PurchaseForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        try:
            order = create_purchase(request.user, form.cleaned_data, uuid.UUID(request.POST.get('request_key','')))
            messages.success(request, 'Purchase order created. Stock will increase only after delivery is received.')
            return redirect('purchase_detail', pk=order.pk)
        except (BusinessError, ValueError, ValidationError, IntegrityError) as error:
            form.add_error(None, error_text(error))
    return render(request, 'purchase_new.html', {'form':form, 'request_key':uuid.uuid4()})


@staff_only
def purchase_detail(request, pk):
    order = get_object_or_404(PurchaseOrder.objects.select_related('movie','wish'), pk=pk)
    error = ''
    if request.method == 'POST':
        try:
            receive_purchase(request.user, pk, int(request.POST.get('quantity','0')),
                uuid.UUID(request.POST.get('request_key','')), request.POST.get('note',''))
            messages.success(request, 'Delivery received. The movie is listed and stock and wishlist status are updated.')
            return redirect('purchase_detail', pk=pk)
        except (BusinessError, ValueError) as exc:
            error = error_text(exc)
    return render(request, 'purchase_detail.html', {'order':order, 'error':error,
        'receipts':order.receipts.select_related('operator').order_by('-created_at'), 'request_key':uuid.uuid4()})
