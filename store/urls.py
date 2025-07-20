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
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]