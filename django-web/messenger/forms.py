from django import forms

class NewMessage(forms.Form):
    msg_text = forms.Textarea()