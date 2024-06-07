from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    # Field for the recipient's full name with custom label and placeholder
    shipping_full_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
        required=True
    )
    # Field for the recipient's email address with custom label and placeholder
    shipping_email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        required=True
    )
    # Field for the shipping address with custom label and placeholder
    shipping_address = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address1'}),
        required=True
    )
    # Field for the shipping city with custom label and placeholder
    shipping_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        required=True
    )
    # Field for the shipping zipcode with custom label and placeholder, not required
    shipping_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
        required=False
    )
    # Field for the shipping country with custom label and placeholder
    shipping_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=True
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name', 'shipping_email', 'shipping_address',
            'shipping_city', 'shipping_zipcode', 'shipping_country'
        ]
        exclude = ['user', ]  # Exclude the 'user' field from the form


class BillingForm(forms.Form):
    # Field for the name on the card with custom label and placeholder
    card_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on card'}),
        required=True
    )
    # Field for the card number with custom label and placeholder
    card_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card number'}),
        required=True
    )
    # Field for the card expiration date with custom label and placeholder
    card_exp_date = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expiration date'}),
        required=True
    )
    # Field for the card CVV code with custom label and placeholder
    card_cvv_number = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV code'}),
        required=True
    )
    # Field for the billing address with custom label and placeholder
    card_address = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing address'}),
        required=True
    )
    # Field for the billing city with custom label and placeholder
    card_city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing city'}),
        required=True
    )
    # Field for the billing zipcode with custom label and placeholder
    card_zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing zipcode'}),
        required=True
    )
    # Field for the billing country with custom label and placeholder
    card_country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Billing country'}),
        required=True
    )
