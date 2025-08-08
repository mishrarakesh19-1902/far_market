from django import forms
from django.contrib.auth.models import User
from .models import (
    FarmerProfile, BuyerProfile, Crop, Contact,
    Product, Order, ProductImage, Review
)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    ROLE_CHOICES = (('farmer', 'Farmer'), ('buyer', 'Buyer'))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    # Farmer Fields
    farm_name = forms.CharField(required=False)
    location = forms.CharField(required=False)
    farmer_contact = forms.CharField(required=False, label="Farmer Contact Number")

    # Buyer Fields
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False, widget=forms.Textarea)
    company_name = forms.CharField(required=False)
    buyer_contact = forms.CharField(required=False, label="Buyer Contact Number")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# ✅ Farmer Profile Form
class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['farm_name', 'location', 'contact_number']
        widgets = {
            'farm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ✅ Buyer Profile Form (✅ FIXED)
class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['phone', 'address', 'company_name', 'contact_number']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ✅ Crop Prediction Form
class CropInputForm(forms.Form):
    nitrogen = forms.FloatField(label='Nitrogen (%)')
    phosphorus = forms.FloatField(label='Phosphorus (%)')
    potassium = forms.FloatField(label='Potassium (%)')
    pH = forms.FloatField(label='pH Level')
    temperature = forms.FloatField(label='Temperature (°C)', required=False)
    humidity = forms.FloatField(label='Humidity (%)', required=False)
    rainfall = forms.FloatField(label='Rainfall (mm)', required=False)

# ✅ Yield Prediction Form
class YieldPredictionForm(forms.Form):
    year = forms.IntegerField(label='Year')
    average_rain_fall_mm_per_year = forms.FloatField(label='Average Rainfall (mm/year)')
    pesticides_tonnes = forms.FloatField(label='Pesticides (tonnes)')
    avg_temp = forms.FloatField(label='Average Temperature (°C)')
    area = forms.CharField(label='Area', max_length=100)
    item = forms.CharField(label='Crop Item', max_length=100)

# ✅ Contact Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ✅ Product Form with Multiple Images
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price_per_unit', 'unit', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ✅ Order Form
PAYMENT_CHOICES = [
    ('COD', 'Cash on Delivery'),
    ('Paytm', 'Paytm'),
    ('PhonePe', 'PhonePe'),
    ('NetBanking', 'Net Banking'),
    ('Card', 'Credit/Debit Card'),
]

class OrderForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter delivery address'})
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'payment_method']

# ✅ Cart Quantity Update Form
class CartQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter quantity',
        })
    )

# ✅ Product Search Form
class ProductSearchForm(forms.Form):
    q = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by product name or seller username',
            'class': 'form-control'
        })
    )

# ✅ Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Write your feedback...'}),
        }
