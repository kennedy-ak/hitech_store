from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.conf import settings
from .models import Product, CartItem, Order, OrderItem, UserProfile, ShippingAddress
from .forms import SignUpForm, CheckoutForm, UserProfileForm, ShippingAddressForm, QuickCheckoutForm
import json
import requests
import uuid

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        return CartItem.objects.filter(session_key=session_key)

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': quantity}
        )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_detail', slug=product.slug)

def cart(request):
    cart_items = get_cart_items(request)
    total = sum(item.total_price for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated!')
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    
    return redirect('cart')

@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')

def checkout(request):
    cart_items = get_cart_items(request)
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    # Check if user is authenticated, if not redirect to login with next parameter
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in or create an account to proceed with checkout.')
        return redirect(f'/login/?next=/checkout/')
    
    total = sum(item.total_price for item in cart_items)
    
    # Get user's saved shipping addresses
    shipping_addresses = request.user.shipping_addresses.all() if hasattr(request.user, 'shipping_addresses') else []
    default_address = shipping_addresses.filter(is_default=True).first()
    
    if request.method == 'POST':
        form = QuickCheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # Create order
            order = Order(user=request.user, total=total, payment_id=str(uuid.uuid4()))
            
            # Handle shipping information
            selected_address = form.cleaned_data.get('shipping_address')
            if selected_address:
                # Use saved address
                order.shipping_name = selected_address.name
                order.shipping_email = selected_address.email
                order.shipping_phone = selected_address.phone
                order.shipping_address = f"{selected_address.address_line_1}, {selected_address.address_line_2}, {selected_address.city}, {selected_address.state}, {selected_address.postal_code}, {selected_address.country}".replace(', ,', ',').strip(', ')
            else:
                # Use manually entered address
                order.shipping_name = form.cleaned_data['shipping_name']
                order.shipping_email = form.cleaned_data['shipping_email']
                order.shipping_phone = form.cleaned_data['shipping_phone']
                order.shipping_address = form.cleaned_data['shipping_address']
            
            order.save()
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear cart
            cart_items.delete()
            
            # Redirect to payment initialization
            return redirect('initialize_payment', order_id=order.id)
    else:
        # Pre-fill form with default address if available
        initial_data = {}
        if default_address:
            initial_data['shipping_address'] = default_address.id
        form = QuickCheckoutForm(initial=initial_data, user=request.user)
    
    return render(request, 'store/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'shipping_addresses': shipping_addresses,
        'default_address': default_address,
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})

@login_required
def profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Handle profile form submission
    if request.method == 'POST' and 'profile_form' in request.POST:
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if profile_form.is_valid():
            # Update user basic info
            request.user.first_name = profile_form.cleaned_data['first_name']
            request.user.last_name = profile_form.cleaned_data['last_name']
            request.user.email = profile_form.cleaned_data['email']
            request.user.save()
            
            # Save profile
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile, user=request.user)
    
    # Handle shipping address form submission
    if request.method == 'POST' and 'address_form' in request.POST:
        address_id = request.POST.get('address_id')
        if address_id:
            # Edit existing address
            try:
                address = ShippingAddress.objects.get(id=address_id, user=request.user)
                address_form = ShippingAddressForm(request.POST, instance=address)
            except ShippingAddress.DoesNotExist:
                messages.error(request, 'Address not found.')
                return redirect('profile')
        else:
            # Create new address
            address_form = ShippingAddressForm(request.POST)
        
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            action = 'updated' if address_id else 'added'
            messages.success(request, f'Shipping address {action} successfully!')
            return redirect('profile')
    else:
        address_form = ShippingAddressForm()
    
    # Get user's orders and shipping addresses
    orders = Order.objects.filter(user=request.user)
    shipping_addresses = ShippingAddress.objects.filter(user=request.user)
    
    context = {
        'profile_form': profile_form,
        'address_form': address_form,
        'orders': orders,
        'shipping_addresses': shipping_addresses,
        'profile': profile,
    }
    
    return render(request, 'store/profile.html', context)

@login_required
@require_POST
def delete_shipping_address(request, address_id):
    try:
        address = ShippingAddress.objects.get(id=address_id, user=request.user)
        address.delete()
        messages.success(request, 'Shipping address deleted successfully!')
    except ShippingAddress.DoesNotExist:
        messages.error(request, 'Address not found.')
    
    return redirect('profile')

@login_required
@require_POST
def set_default_address(request, address_id):
    try:
        # Remove default from all user addresses
        ShippingAddress.objects.filter(user=request.user).update(is_default=False)
        
        # Set new default
        address = ShippingAddress.objects.get(id=address_id, user=request.user)
        address.is_default = True
        address.save()
        
        messages.success(request, 'Default shipping address updated!')
    except ShippingAddress.DoesNotExist:
        messages.error(request, 'Address not found.')
    
    return redirect('profile')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            
            # Check if there's a next parameter to redirect back to checkout
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def initialize_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Build callback URL
    callback_url = request.build_absolute_uri(f'/payment/callback/?reference={order.payment_id}')
    
    try:
        payment_url = initiate_payment(order, callback_url)
        return redirect(payment_url)
    except Exception as e:
        messages.error(request, f'Payment initialization failed: {str(e)}')
        return redirect('order_confirmation', order_id=order.id)

def payment_callback(request):
    ref = request.GET.get('reference')
    if not ref:
        messages.error(request, 'Invalid payment reference')
        return redirect('home')
    
    try:
        order = Order.objects.get(payment_id=ref)
        if verify_payment(ref):
            order.payment_status = 'completed'
            order.status = 'processing'
            order.save()
            
            messages.success(request, f'Payment successful! Order #{order.id} confirmed.')
            return redirect('order_confirmation', order_id=order.id)
        else:
            order.payment_status = 'failed'
            order.save()
            messages.error(request, 'Payment verification failed')
            return redirect('order_confirmation', order_id=order.id)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('home')
    except Exception as e:
        messages.error(request, f'Payment verification error: {str(e)}')
        return redirect('home')

def initiate_payment(order, callback_url):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": order.shipping_email,
        "amount": int(order.total * 100),  # Convert to pesewas for GHS
        "currency": "GHS",
        "reference": order.payment_id,
        "callback_url": callback_url
    }
    response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()['data']
        return data['authorization_url']
    else:    
        error_message = response.json().get('message', 'No error message received')
        raise Exception(f"Payment initialization failed with Paystack: {error_message}")

def verify_payment(payment_id):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://api.paystack.co/transaction/verify/{payment_id}", headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        return data['status'] == 'success'
    else:
        raise Exception("Failed to verify payment")