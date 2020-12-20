from django import forms
from phone_field import PhoneField

PAYMENT_CHIOCE= (
    ('S','Stripe'),
    ('P','Paypal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '4-Killo'
    }))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '4-Killo'
    }),required=False)
    unique_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '4-Killo'
    }))
    phone = PhoneField(blank=True, help_text='Contact phone number').formfield()

