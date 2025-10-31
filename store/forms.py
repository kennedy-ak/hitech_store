from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, UserProfile, ShippingAddress

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address']
        widgets = {
            'shipping_name': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'email', 'phone', 'address_line_1', 'address_line_2', 
                 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class QuickCheckoutForm(forms.Form):
    shipping_address = forms.ModelChoiceField(
        queryset=ShippingAddress.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select saved address or enter new one"
    )
    
    # Manual address fields (used when no saved address is selected)
    shipping_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    shipping_phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    shipping_address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shipping_address'].queryset = user.shipping_addresses.all()
