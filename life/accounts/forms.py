from django import forms
from .models import Organization
from django.contrib.auth import  get_user_model

class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(min_value = 1, max_digits = 10, decimal_places=2)


User = get_user_model()
#this form takes a username and password 
class OrganizationCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Organization
        fields = ["name"]