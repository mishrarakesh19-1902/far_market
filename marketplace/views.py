

# views.py (arranged in logical order)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.conf import settings
from django import forms
from django.db.models import Q

import os
import pickle
import pandas as pd
from decimal import Decimal

from .models import (
    Product, ProductImage, Review, CartItem, Order,
    UserProfile, FarmerProfile, BuyerProfile, Crop, CropPrice
)
from .forms import (
    OrderForm, ProductSearchForm, UserRegistrationForm,
    FarmerProfileForm, BuyerProfileForm, ContactForm,
    CropInputForm, YieldPredictionForm, ProductForm
)

# ========== AUTHENTICATION ==========
def home(request):
    return render(request, 'marketplace/index.html')

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

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

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data['password']
            role = request.POST.get('role')
            if not role:
                messages.error(request, "Please select a role (Farmer or Buyer).")
                return redirect('register')
            user.set_password(raw_password)
            user.save()
            UserProfile.objects.create(user=user, role=role)
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'marketplace/register.html', {'user_form': form})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             role = UserProfile.objects.get(user=user).role
#             return redirect('farmer_dashboard' if role == 'farmer' else 'buyer_dashboard')
#         else:
#             messages.error(request, "Invalid credentials")
#     return render(request, 'marketplace/login.html', {'form': ''})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            try:
                role = UserProfile.objects.get(user=user).role
                if role == 'farmer':
                    messages.success(request, "Welcome to Farmer Dashboard")
                    return redirect('farmer_dashboard')
                elif role == 'buyer':
                    messages.success(request, "Welcome to Buyer Dashboard")
                    return redirect('buyer_dashboard')
                else:
                    messages.error(request, "Unknown role")
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'marketplace/login.html', {'form': ''})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# ========== HOMEPAGE & DASHBOARDS ==========



@login_required
def farmer_dashboard(request):
    if UserProfile.objects.get(user=request.user).role != 'farmer':
        return redirect('login')
    return render(request, 'marketplace/farmer_dashboard.html', {'is_farmer': True})

@login_required
def buyer_dashboard(request):
    if UserProfile.objects.get(user=request.user).role != 'buyer':
        return redirect('login')
    return render(request, 'marketplace/buyer_dashboard.html', {'is_farmer': False})

# ========== PRODUCT MANAGEMENT ==========

@login_required
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            for img in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=img)
            return redirect('farmer_dashboard')
    else:
        form = ProductForm()
    return render(request, 'direct-selling/upload_product.html', {'form': form})

@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'direct-selling/my_products.html', {'products': products})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'direct-selling/edit_product.html', {'form': form, 'product': product})

def product_list(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.select_related('seller').all()
    if form.is_valid() and form.cleaned_data['q']:
        query = form.cleaned_data['q']
        products = products.filter(
            Q(name__icontains=query) |
            Q(seller__username__icontains=query)
        )
    return render(request, 'direct-selling/product_list.html', {'products': products, 'form': form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()
    return redirect('my_products')  # make sure 'my_products' is your name in urls.py

@login_required
@require_http_methods(["GET", "POST"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = product.images.all()
    reviews = product.reviews.order_by('-created_at')
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
            messages.success(request, 'Review submitted successfully.')
            return redirect('product_detail', pk=pk)
    return render(request, 'direct-selling/product_detail.html', {'product': product, 'images': images, 'reviews': reviews})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user:
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    else:
        messages.error(request, 'You can only delete your own review.')
    return redirect('product_detail', pk=review.product.pk)

# ========== CART AND ORDER ==========

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, _ = CartItem.objects.get_or_create(user=request.user, product=product)
    cart_item.unit = request.POST.get("unit", product.unit)
    cart_item.quantity = cart_item.quantity or 1
    cart_item.save()
    return redirect(request.GET.get('next') or 'product_list')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        item.item_total_price = (item.product.price_per_unit or Decimal('0.00')) * (item.quantity or 0)
    total_price = sum(item.item_total_price for item in cart_items)
    return render(request, 'direct-selling/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'form': OrderForm()})

@login_required
@require_POST
def update_cart(request):
    for item in CartItem.objects.filter(user=request.user):
        try:
            qty = int(request.POST.get(f'quantity_{item.id}', '').strip() or 1)
            item.quantity = qty
            item.unit = request.POST.get(f'unit_{item.id}', '').strip() or item.unit
            item.save()
        except (ValueError, TypeError):
            continue
    messages.success(request, "Cart updated successfully.")
    return redirect('cart')

@login_required
@require_POST
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')
    form = OrderForm(request.POST)
    if form.is_valid():
        for item in cart_items:
            Order.objects.create(
                buyer=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=item.product.price_per_unit * item.quantity,
                **form.cleaned_data
            )
        cart_items.delete()
        messages.success(request, "✅ Your order has been placed successfully.")
        return redirect('order_success')
    messages.error(request, "❌ Please correct the errors in the shipping form.")
    return render(request, 'direct-selling/cart.html', {'cart_items': cart_items, 'total_price': sum(item.item_total_price for item in cart_items), 'form': form})

@login_required
def delete_cart_item(request, item_id):
    get_object_or_404(CartItem, id=item_id, user=request.user).delete()
    return redirect('cart')

@login_required
def order_success(request):
    return render(request, 'direct-selling/order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'direct-selling/my_orders.html', {'orders': orders})

@login_required
def farmer_orders(request):
    orders = Order.objects.filter(product__seller=request.user).order_by('-created_at')
    return render(request, 'direct-selling/farmer_orders.html', {'orders': orders})

@login_required
@require_POST
def mark_order_completed(request, order_id):
    order = get_object_or_404(Order, id=order_id, product__seller=request.user)
    if order.status != 'Completed':
        order.status = 'Completed'
        order.save()
        messages.success(request, f"Order #{order.id} marked as completed.")
    return redirect('farmer_orders')

# ========== OTHER FEATURES ==========

# @login_required
# def profile(request):
#     profile = FarmerProfile.objects.filter(user=request.user).first()
#     return render(request, 'marketplace/profile.html', {'profile': profile})
# aaj yaha pe change kiye h 
@login_required
def profile(request):
    user = request.user
    role = user.userprofile.role  # Assuming you have a UserProfile model connected to User

    if role == "farmer":
        profile = FarmerProfile.objects.filter(user=user).first()
    elif role == "buyer":
        profile = BuyerProfile.objects.filter(user=user).first()
    else:
        profile = None

    return render(request, 'marketplace/profile.html', {
        'user': user,
        'role': role,
        'profile': profile
    })




@login_required
def crop_price_view(request):
    crop_prices = CropPrice.objects.all().order_by('crop_name')
    return render(request, 'marketplace/crop_price.html', {'crop_prices': crop_prices})

# Crop Prediction
with open(os.path.join(settings.BASE_DIR, 'ml_models', 'minmaxscaler.pkl'), 'rb') as f:
    scaler = pickle.load(f)
with open(os.path.join(settings.BASE_DIR, 'ml_models', 'model.pkl'), 'rb') as f:
    model = pickle.load(f)

LABEL_TO_CROP = {1: 'rice', 2: 'maize', 3: 'jute', 4: 'cotton', 5: 'coconut', 6: 'papaya', 7: 'orange', 8: 'apple', 9: 'muskmelon', 10: 'watermelon', 11: 'grapes', 12: 'mango', 13: 'banana', 14: 'pomegranate', 15: 'lentil', 16: 'blackgram', 17: 'mungbean', 18: 'mothbeans', 19: 'pigeonpeas', 20: 'kidneybeans', 21: 'chickpea', 22: 'coffee'}

@login_required
def predict_crop(request):
    result, input_values = None, None
    if request.method == 'POST':
        form = CropInputForm(request.POST)
        if form.is_valid():
            input_values = form.cleaned_data
            data = [
                input_values['nitrogen'], input_values['phosphorus'],
                input_values['potassium'], input_values['pH'],
                input_values.get('temperature', 0),
                input_values.get('humidity', 0),
                input_values.get('rainfall', 0)
            ]
            scaled = scaler.transform([data])
            prediction = model.predict(scaled)[0]
            result = LABEL_TO_CROP.get(prediction, 'Unknown Crop')
            form = CropInputForm()
    else:
        form = CropInputForm()
    return render(request, 'marketplace/predict_crop.html', {'form': form, 'result': result, 'input_values': input_values})

# Yield Prediction
with open(os.path.join(settings.BASE_DIR, 'ml_models', 'dtr.pkl'), 'rb') as f:
    yield_model = pickle.load(f)
with open(os.path.join(settings.BASE_DIR, 'ml_models', 'preprocessor.pkl'), 'rb') as f:
    preprocessor = pickle.load(f)

@login_required
def yeild_predict(request):
    prediction, entered_data = None, None
    if request.method == 'POST':
        form = YieldPredictionForm(request.POST)
        if form.is_valid():
            entered_data = form.cleaned_data
            df = pd.DataFrame([{
                'Year': entered_data['year'],
                'average_rain_fall_mm_per_year': entered_data['average_rain_fall_mm_per_year'],
                'pesticides_tonnes': entered_data['pesticides_tonnes'],
                'avg_temp': entered_data['avg_temp'],
                'Area': entered_data['area'],
                'Item': entered_data['item']
            }])
            X = preprocessor.transform(df)
            prediction = round(yield_model.predict(X)[0], 2)
            form = YieldPredictionForm()
    else:
        form = YieldPredictionForm()
    return render(request, 'marketplace/yield_predict.html', {'form': form, 'prediction': prediction, 'entered_data': entered_data})

@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for contacting us. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'marketplace/contact.html', {'form': form})

