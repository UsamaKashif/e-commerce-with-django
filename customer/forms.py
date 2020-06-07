from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms


class CustomerForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True)
    class Meta:
        model = User
        fields = ["username","name","email","password1","password2"]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Account with that email already exists")
        return email



class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (
        ("S","Stripe"),
        ("P","PayPal")
    )
    street = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder":"234 Main St",
            "class":"form-control",
            "id":"address"
        }
    ))
    apartment = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder":"Apartment or suite",
            "class":"form-control",
            "id":"address-2"
        }
    ))
    city = forms.CharField()
    zip_code = forms.CharField()

