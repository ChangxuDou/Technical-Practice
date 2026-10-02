import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer
from movies.models import Movie

def normalize_phone(value):
    value=re.sub(r'[\s()\-]','',value)
    if not re.fullmatch(r'\+?\d{6,20}',value):raise forms.ValidationError('Enter a valid phone number (6–20 digits, optionally starting with +).')
    return value

class SignupForm(UserCreationForm):
    full_name=forms.CharField(label='Full name',max_length=100)
    phone=forms.CharField(label='Phone',max_length=30)
    email=forms.EmailField(label='Email')
    class Meta:
        model=User
        fields=['username','full_name','phone','email','password1','password2']
    def clean_phone(self):
        phone=normalize_phone(self.cleaned_data['phone'])
        if Customer.objects.filter(phone=phone).exists():raise forms.ValidationError('This phone number is already registered. Ask a staff member to link your account.')
        return phone

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['full_name','phone','email','active']
    def clean_phone(self):return normalize_phone(self.cleaned_data['phone'])

class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['title','release_year','genre','daily_rate','total_quantity','barcode','director','runtime','synopsis','active']
        widgets={'synopsis':forms.Textarea(attrs={'rows':4})}
    def clean_release_year(self):
        year=self.cleaned_data['release_year']
        if not 1888<=year<=2100:raise forms.ValidationError('The year must be between 1888 and 2100.')
        return year
    def clean_total_quantity(self):
        total=self.cleaned_data['total_quantity']
        if total>100000:raise forms.ValidationError('Total stock cannot exceed 100,000.')
        return total

from decimal import Decimal
from .models import RewardPolicy, MovieWish
from movies.models import Genre

class WishForm(forms.Form):
    title = forms.CharField(label='Movie title', max_length=255)
    release_year = forms.IntegerField(label='Release year', min_value=1888, max_value=2100)
    note = forms.CharField(label='Director, edition or reason for requesting (optional)', max_length=500, required=False, widget=forms.Textarea(attrs={'rows':3}))

class TopUpForm(forms.Form):
    amount = forms.DecimalField(label='Top-up amount (EUR)', min_value=1, max_value=10000, max_digits=7, decimal_places=2, widget=forms.NumberInput(attrs={'step':'0.01'}))

class RewardPolicyForm(forms.ModelForm):
    money_unit = forms.DecimalField(label='For every EUR', min_value=Decimal('0.01'), max_value=10000, max_digits=8, decimal_places=2)
    points_unit = forms.IntegerField(label='Award this many points', min_value=1, max_value=10000)
    class Meta:
        model = RewardPolicy
        fields = ['money_unit','points_unit','enabled']

class PurchaseForm(forms.Form):
    wish = forms.ModelChoiceField(label='Linked wishlist request (optional)', queryset=MovieWish.objects.all(), required=False)
    movie = forms.ModelChoiceField(label='Restock an existing movie (leave blank for a new movie)', queryset=Movie.objects.all(), required=False)
    title = forms.CharField(label='New movie title', max_length=255, required=False)
    release_year = forms.IntegerField(label='New movie release year', min_value=1888, max_value=2100, required=False)
    genre = forms.ModelChoiceField(label='New movie genre', queryset=Genre.objects.all(), required=False)
    barcode = forms.RegexField(label='New movie 10-digit barcode', regex=r'^\d{10}$', required=False)
    daily_rate = forms.DecimalField(label='New movie daily rate (EUR)', min_value=Decimal('0.01'), max_value=Decimal('9999.99'), max_digits=6, decimal_places=2, required=False)
    quantity = forms.IntegerField(label='Copies to purchase', min_value=1, max_value=10000, initial=5)
    unit_cost = forms.DecimalField(label='Unit purchase cost (EUR, record only)', min_value=0, max_value=Decimal('999999.99'), max_digits=8, decimal_places=2, initial=0)
    supplier = forms.CharField(label='Supplier (optional)', max_length=120, required=False)

    def clean(self):
        data = super().clean()
        wish = data.get('wish')
        has_movie = data.get('movie') or (wish and wish.movie_id)
        if not has_movie:
            needed = ['genre','barcode','daily_rate']
            if not wish:
                needed += ['title','release_year']
            for name in needed:
                if not data.get(name):
                    self.add_error(name, 'Required when adding a new movie.')
        return data
