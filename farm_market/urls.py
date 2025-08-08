# from django.contrib import admin
# from django.urls import path
# from marketplace import views
# from marketplace.views import contact_view
# from django.conf import settings
# from django.conf.urls.static import static
# # from django.conf import settings
# # from django.conf.urls.static import static

# urlpatterns = [
#     path('admin12/', admin.site.urls),
#     path('', views.home, name='home'),  # Homepage
#     path('register/', views.register_view, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('', views.product_list, name='product_list'),     
#     path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
#     path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
#     path('profile/', views.profile, name='profile'),  # User Profile 
#     path('predict-crop/', views.predict_crop, name='predict_crop'),
#     path('yeild-predict/', views.yeild_predict, name='yeild_predict'),
#     path('contact/', views.contact_view, name='contact'),
#     path('crop_price/', views.crop_price_view, name='crop_prices'),
#     path('direct-selling/upload/', views.upload_product, name='upload_product'),
#     path('direct-selling/', views.product_list, name='product_list'),
#     path('direct-selling/<int:pk>/', views.product_detail, name='product_detail'),
#     path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/', views.cart, name='cart'),
    
#     path('order/success/', views.order_success, name='order_success'),
#     path('order/<int:order_id>/complete/', views.mark_order_completed, name='mark_order_completed'),

#     path('my_orders/', views.my_orders, name='my_orders'),
#     path('farmer_orders/', views.farmer_orders, name='farmer_orders'),
    
#     path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
#     path('farmer/my-products/', views.my_products, name='my_products'),

#     path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),

# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.contrib import admin
from django.urls import path
from marketplace import views
from marketplace.views import contact_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin12/', admin.site.urls),

    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),

    # Profile & Contact
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact_view, name='contact'),

    # Crop Prediction & Prices
    path('predict-crop/', views.predict_crop, name='predict_crop'),
    path('yeild-predict/', views.yeild_predict, name='yeild_predict'),
    path('crop_price/', views.crop_price_view, name='crop_prices'),


    # Product CRUD & Listing
    path('direct-selling/', views.product_list, name='product_list'),
    path('direct-selling/upload/', views.upload_product, name='upload_product'),
    path('direct-selling/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),

    # urls.py
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    # Cart & Order
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/update/', views.update_cart, name='update_cart'),  # POST update
    path('order/place/', views.place_order, name='place_order'),  # POST place order
    path('order/success/', views.order_success, name='order_success'),
    path('order/<int:order_id>/complete/', views.mark_order_completed, name='mark_order_completed'),

    # Orders Views
    path('my_orders/', views.my_orders, name='my_orders'),
    path('farmer_orders/', views.farmer_orders, name='farmer_orders'),

    # Product Management
    path('farmer/my-products/', views.my_products, name='my_products'),

    # ✅ New route for deleting a review
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


