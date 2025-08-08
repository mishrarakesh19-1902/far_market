# # marketplace/urls.py
# from django.urls import path
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static
# urlpatterns = [
#     path('', views.CropListView.as_view(), name='crop_list'),
#     path('crop/<int:crop_id>/', views.crop_detail, name='crop_detail'),
#     path('add_crop/', views.CropCreateView.as_view(), name='add_crop'),
    
#     path('predict-crop/', views.predict_crop, name='predict_crop'),
#     path('register/', views.register, name='register'),  # Registration 
#     path('login/', views.user_login, name='login'),  # Login
#     path('profile/', views.profile, name='profile'),  # User Profile
    
#     path('', views.home, name='home'),
#     path('contact/', views.contact_view, name='contact'),
#     path('crop_price/', views.crop_price_view, name='crop_prices'),
#     path('direct-selling/upload/', views.upload_product, name='upload_product'),
#     path('direct-selling/', views.product_list, name='product_list'),
#     path('direct-selling/<int:pk>/', views.product_detail, name='product_detail'),
#     path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/', views.cart, name='cart'),
#     path('place_order/<int:product_id>/', views.place_order, name='place_order'),
#     path('my_orders/', views.my_orders, name='my_orders'),
#     path('farmer_orders/', views.farmer_orders, name='farmer_orders'),
#     path('cart/increase/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
#     path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
#     path('cart/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),

# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
