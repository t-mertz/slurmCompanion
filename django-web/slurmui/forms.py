from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
    input_name = forms.CharField(label="Username", required=True)
    input_password = forms.CharField(label="Password", required=True, widget=widgets.PasswordInput)