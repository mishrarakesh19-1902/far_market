from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from cloudinary.models import CloudinaryField
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=(('farmer', 'Farmer'), ('buyer', 'Buyer')))

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.farm_name


class Crop(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE)
    crop_name = models.CharField(max_length=100, default="Unknown Crop")
    quantity = models.IntegerField(default=0)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    harvest_date = models.DateField()

    def __str__(self):
        return f"{self.crop_name} ({self.farmer.farm_name})"


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    company_name = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


class CropPrice(models.Model):
    crop_name = models.CharField(max_length=100)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.crop_name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer_products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.price_per_unit is None:
            self.price_per_unit = Decimal('0.00')


# ✅ New: For Multiple Images per Product
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='product_images/')

#     def __str__(self):
#         return f"Image for {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')  # ✅ Cloudinary storage

    def __str__(self):
        return f"Image for {self.product.name}"





# ✅ Updated: Unit field added
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=20, null=True, blank=True)  # New field for per item unit

    def __str__(self):
        return f"{self.quantity} {self.unit or ''} of {self.product.name}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.TextField(null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    payment_method = models.CharField(max_length=20, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"


# ✅ New: Review model
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"
