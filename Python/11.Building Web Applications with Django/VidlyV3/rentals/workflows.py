"""Wishlist, approved purchasing and a local sandbox payment workflow."""
import hashlib
import unicodedata
import uuid
from datetime import timedelta
from decimal import Decimal, ROUND_DOWN
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from movies.models import Movie
from .models import (Customer, Ledger, RewardPolicy, PolicyRevision, TopUp,
                     PointsEntry, MovieWish, WishRequest, PurchaseOrder, StockReceipt)
from .services import BusinessError, is_staff, is_manager


def canonical_title(title):
    return ' '.join(unicodedata.normalize('NFKC', title).split()).casefold()


def wish_key(title, year):
    return hashlib.sha256(f'{canonical_title(title)}|{year}'.encode()).hexdigest()


def policy_data(policy):
    return {'money_unit': str(policy.money_unit), 'points_unit': policy.points_unit,
            'enabled': policy.enabled}


def reward_for(amount, money_unit, points_unit):
    return int((amount / money_unit * points_unit).to_integral_value(rounding=ROUND_DOWN))


@transaction.atomic
def configure_rewards(user, money_unit, points_unit, enabled):
    if not is_manager(user):
        raise PermissionDenied
    policy, _ = RewardPolicy.objects.select_for_update().get_or_create(pk=1)
    before = policy_data(policy)
    policy.money_unit, policy.points_unit = money_unit, points_unit
    policy.enabled, policy.updated_by = enabled, user
    policy.full_clean()
    policy.save()
    PolicyRevision.objects.create(operator=user, before=before, after=policy_data(policy))
    return policy


@transaction.atomic
def start_topup(user, amount, key):
    customer = Customer.objects.select_for_update().get(user=user)
    existing = TopUp.objects.filter(request_key=key).first()
    if existing:
        if existing.customer_id != customer.pk:
            raise PermissionDenied
        return existing
    policy, _ = RewardPolicy.objects.get_or_create(pk=1)
    if not customer.active or not policy.enabled:
        raise BusinessError('Top-ups are unavailable: the customer is inactive or top-ups are paused.')
    if not amount.is_finite() or not Decimal('1') <= amount <= Decimal('10000') or amount.as_tuple().exponent < -2:
        raise BusinessError('Top up between €1 and €10,000, with up to two decimal places.')
    points = reward_for(amount, policy.money_unit, policy.points_unit)
    if points > 2147483647 or points + customer.points > 2147483647:
        raise BusinessError('This award exceeds the points limit. Ask the manager to adjust the policy.')
    return TopUp.objects.create(customer=customer, amount=amount, money_unit=policy.money_unit,
        points_unit=policy.points_unit, awarded_points=points, request_key=key)


class MockPaymentGateway:
    """Local test gateway. No network, real bank or card data is involved."""
    @staticmethod
    def process(order, outcome):
        if outcome not in {'success', 'failed', 'cancelled'}:
            raise BusinessError('Choose a simulated payment outcome.')
        return {'status': outcome, 'reference': 'MOCK-' + uuid.uuid4().hex}


@transaction.atomic
def finish_topup(user, order_id, outcome):
    order = TopUp.objects.select_for_update().select_related('customer').get(pk=order_id)
    # Even a manager must not submit another customer's payment simulation.
    if order.customer.user_id != user.pk:
        raise PermissionDenied
    if order.status != 'pending':
        return order
    customer = Customer.objects.select_for_update().get(pk=order.customer_id)
    if not customer.active:
        raise BusinessError('This account is inactive. Please contact a staff member.')
    if timezone.now() >= order.created_at + timedelta(minutes=30):
        order.status = 'expired'
        order.completed_at = timezone.now()
        order.save(update_fields=['status', 'completed_at'])
        return order
    result = MockPaymentGateway.process(order, outcome)
    if result['status'] == 'success':
        if customer.balance + order.amount > Decimal('99999999.99') or customer.points + order.awarded_points > 2147483647:
            raise BusinessError('The balance or points limit would be exceeded.')
        customer.balance += order.amount
        customer.points += order.awarded_points
        customer.save(update_fields=['balance', 'points'])
        entry = Ledger.objects.create(customer=customer, operator=user, kind='recharge',
            amount=order.amount, balance_after=customer.balance, request_key=order.request_key,
            note=f'Customer simulated payment {order.pk}')
        PointsEntry.objects.create(customer=customer, ledger=entry, delta=order.awarded_points,
            points_after=customer.points, note=f'Top-up reward: every €{order.money_unit} awards {order.points_unit} points')
    order.status = result['status']
    order.provider_reference = result['reference']
    order.completed_at = timezone.now()
    order.save(update_fields=['status', 'provider_reference', 'completed_at'])
    return order


def reverse_refund_points(customer, amount, ledger):
    """Called inside adjust_balance's transaction; reverse oldest reward lots first."""
    remaining, reversed_total = amount, 0
    for topup in TopUp.objects.select_for_update().filter(customer=customer, status='success',
            refunded_amount__lt=F('amount')).order_by('completed_at', 'id'):
        part = min(remaining, topup.amount - topup.refunded_amount)
        topup.refunded_amount += part
        new_reversed = int(topup.awarded_points * topup.refunded_amount / topup.amount)
        reversed_total += new_reversed - topup.reversed_points
        topup.reversed_points = new_reversed
        topup.save(update_fields=['refunded_amount', 'reversed_points'])
        remaining -= part
        if remaining == 0:
            break
    if reversed_total:
        customer.points -= reversed_total
        customer.save(update_fields=['points'])
        PointsEntry.objects.create(customer=customer, ledger=ledger, delta=-reversed_total,
            points_after=customer.points, note='Balance refund: original top-up rewards reversed proportionally')


@transaction.atomic
def submit_wish(user, title, release_year, note):
    year = release_year
    customer = Customer.objects.get(user=user)
    if not customer.active:
        raise BusinessError('This account is inactive.')
    title = ' '.join(unicodedata.normalize('NFKC', title).split())
    if not title or len(title) > 255 or not 1888 <= year <= 2100 or len(note) > 500:
        raise BusinessError('Enter a valid title, release year and additional information.')
    # Match case and whitespace independent titles within the requested year.
    for movie in Movie.objects.filter(release_year=year):
        if canonical_title(movie.title) == canonical_title(title):
            pending = MovieWish.objects.filter(movie=movie, normalized_key=wish_key(title, year)).first()
            if pending and pending.status == 'planned':
                break
            raise BusinessError('This movie is already in the catalog. Check availability or ask staff to restock it.')
    wish, _ = MovieWish.objects.get_or_create(normalized_key=wish_key(title, year),
        defaults={'title': title, 'release_year': year})
    request, created = WishRequest.objects.get_or_create(customer=customer, wish=wish, defaults={'note':note})
    return request, created


@transaction.atomic
def decline_wish(user, wish_id, note):
    if not is_manager(user):
        raise PermissionDenied
    wish = MovieWish.objects.select_for_update().get(pk=wish_id)
    if wish.status != 'requested':
        raise BusinessError('Only requests under review can be marked as not planned.')
    wish.status, wish.manager_note = 'declined', note[:500]
    wish.save(update_fields=['status','manager_note'])
    return wish


@transaction.atomic
def create_purchase(user, data, key):
    if not is_manager(user):
        raise PermissionDenied
    existing = PurchaseOrder.objects.filter(request_key=key).first()
    if existing:
        return existing
    wish = MovieWish.objects.select_for_update().get(pk=data['wish'].pk) if data.get('wish') else None
    movie = data.get('movie')
    quantity, cost = data['quantity'], data['unit_cost']
    if not 1 <= quantity <= 10000 or cost < 0:
        raise BusinessError('Invalid purchase quantity or cost.')
    if wish and wish.movie_id:
        if movie and movie.pk != wish.movie_id:
            raise BusinessError('This wish is linked to another movie. Select the linked movie.')
        movie = wish.movie
    if movie:
        movie = Movie.objects.select_for_update().get(pk=movie.pk)
        if wish and (canonical_title(movie.title) != canonical_title(wish.title) or movie.release_year != wish.release_year):
            raise BusinessError('The selected movie does not match the requested title and year.')
    else:
        title = wish.title if wish else data['title']
        year = wish.release_year if wish else data['release_year']
        if any(canonical_title(m.title) == canonical_title(title) for m in Movie.objects.filter(release_year=year)):
            raise BusinessError('This movie already exists. Select it to arrange a restock.')
        movie = Movie(title=title, release_year=year, genre=data['genre'], barcode=data['barcode'],
            daily_rate=data['daily_rate'], number_in_stock=0, total_quantity=0, active=False, runtime=0)
        movie.full_clean()
        movie.save()
    purchase = PurchaseOrder.objects.create(movie=movie, wish=wish, quantity=quantity,
        unit_cost=cost, supplier=data['supplier'], operator=user, request_key=key)
    if wish:
        wish.movie = movie
        wish.status = 'available' if movie.available else 'planned'
        wish.manager_note = 'Purchase order created. Awaiting delivery and inspection.'
        wish.save(update_fields=['movie','status','manager_note'])
    return purchase


@transaction.atomic
def receive_purchase(user, purchase_id, quantity, key, note=''):
    if not is_staff(user):
        raise PermissionDenied
    purchase = PurchaseOrder.objects.select_for_update().get(pk=purchase_id)
    existing = StockReceipt.objects.filter(request_key=key).first()
    if existing:
        if existing.purchase_id != purchase.pk:
            raise PermissionDenied
        return existing
    if not isinstance(quantity, int) or not 1 <= quantity <= purchase.remaining:
        raise BusinessError('The received quantity must be greater than 0 and cannot exceed the outstanding delivery.')
    movie = Movie.objects.select_for_update().get(pk=purchase.movie_id)
    if movie.total_quantity + quantity > 100000:
        raise BusinessError('Total stock after receipt cannot exceed 100,000.')
    movie.total_quantity += quantity
    movie.number_in_stock += quantity
    movie.active = True
    movie.save(update_fields=['total_quantity','number_in_stock','active'])
    purchase.received_quantity += quantity
    purchase.save(update_fields=['received_quantity'])
    MovieWish.objects.filter(movie=movie).update(status='available', manager_note='This movie has arrived and is now available in the catalog.')
    return StockReceipt.objects.create(purchase=purchase, quantity=quantity, operator=user, request_key=key, note=note[:255])
