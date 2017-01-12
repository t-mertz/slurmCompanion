from django import forms
from django.forms import widgets
from sshcomm.models import RemoteServer

class LoginForm(forms.Form):
    input_name = forms.CharField(label="Username", required=True)
    input_password = forms.CharField(label="Password", required=True, widget=widgets.PasswordInput)


class AddSshServerForm(forms.Form):
    select_name = forms.ChoiceField(label="Name", choices=RemoteServer.get_installed_servers, required=True)
    input_username = forms.CharField(label="SSH Username", required=True)
    input_password = forms.CharField(label="SSH Password", required=True, widget=widgets.PasswordInput, help_text="Your password and username will be encrypted.")
    input_loc_password = forms.CharField(label="Web Password", required=True, widget=widgets.PasswordInput, 
                        help_text="We need your account password for this website to encrypt your information.")

class AddNewSshServerForm(forms.Form):
    input_name = forms.CharField(label="Name", required=True)
    input_url = forms.CharField(label="URL", required=True)