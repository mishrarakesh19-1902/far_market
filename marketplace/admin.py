from django.contrib import admin
from .models import (
    FarmerProfile, Crop, BuyerProfile, CropPrice, Contact,
    Product, ProductImage, Order, CartItem, Review
)

# Inline admin to allow uploading multiple images for a product from the admin panel
class ProductImageInline(admin.TabularInline):  # You can use StackedInline for a vertical layout
    model = ProductImage
    extra = 1  # Show one extra blank image form
    max_num = 10  # Optional: limit to 10 images per product

# Customize the Product admin view
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'price_per_unit', 'quantity', 'unit', 'location', 'posted_on')
    list_filter = ('seller', 'location', 'posted_on')
    search_fields = ('name', 'description', 'location', 'seller__username')
    inlines = [ProductImageInline]

# Customize the Order admin view
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username', 'product__name')

# Customize the Review admin view
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')

# Register all models
admin.site.register(FarmerProfile)
admin.site.register(Crop)
admin.site.register(BuyerProfile)
admin.site.register(CropPrice)
admin.site.register(Contact)
admin.site.register(Product, ProductAdmin)         # Custom admin with image inline
admin.site.register(ProductImage)                  # Standalone image model (optional)
admin.site.register(Order, OrderAdmin)             # Custom Order admin
admin.site.register(CartItem)
admin.site.register(Review, ReviewAdmin)           # Custom Review admin
