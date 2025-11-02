from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/initialize/<int:order_id>/', views.initialize_payment, name='initialize_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('profile/', views.profile, name='profile'),
    path('profile/address/delete/<int:address_id>/', views.delete_shipping_address, name='delete_shipping_address'),
    path('profile/address/default/<int:address_id>/', views.set_default_address, name='set_default_address'),
    
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Admin Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/products/', views.admin_products, name='admin_products'),
    path('admin-dashboard/products/add/', views.admin_add_product, name='admin_add_product'),
    path('admin-dashboard/products/edit/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('admin-dashboard/products/delete/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),
    path('admin-dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('admin-dashboard/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-dashboard/orders/<int:order_id>/update-status/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin-dashboard/low-stock/', views.admin_low_stock, name='admin_low_stock'),
]