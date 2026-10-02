from django.db import models
from django.db.models import Q, F
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from decimal import Decimal

class Genre(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self): return self.name

class Movie(models.Model):
    title = models.CharField('Title', max_length=255)
    release_year = models.IntegerField('Release year')
    number_in_stock = models.PositiveIntegerField('Available stock', default=0)
    total_quantity = models.PositiveIntegerField('Total stock', default=0)
    daily_rate = models.DecimalField('Daily rate', max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, verbose_name='Genre')
    date_created = models.DateTimeField(default=timezone.now)
    barcode = models.CharField('10-digit barcode', max_length=10, unique=True, null=True, validators=[RegexValidator(r'^\d{10}$','Enter exactly 10 digits.')])
    active = models.BooleanField('Listed', default=True)
    synopsis = models.TextField('Synopsis', blank=True)
    director = models.CharField('Director', max_length=120, blank=True)
    runtime = models.PositiveIntegerField('Runtime (minutes)', default=120)
    artwork = models.CharField(max_length=40, default='orbit')
    class Meta:
        ordering=['id']
        constraints=[models.CheckConstraint(condition=Q(number_in_stock__lte=F('total_quantity')),name='stock_not_above_total'),models.CheckConstraint(condition=Q(daily_rate__gt=0),name='positive_daily_rate')]
    def __str__(self): return self.title
    @property
    def available(self): return self.active and self.number_in_stock > 0
