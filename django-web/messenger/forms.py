from django import forms

class NewMessageForm(forms.Form):
    msg_text = forms.CharField(widget=forms.widgets.Textarea())
    recipient = forms.ChoiceField(choices=()) # choices should be (Contact.user==current_user).contact