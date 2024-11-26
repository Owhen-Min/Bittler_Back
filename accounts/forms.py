from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    nickname = forms.CharField(required=True)
    first_name = forms.CharField(required=True) 