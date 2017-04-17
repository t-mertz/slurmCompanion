from django import forms
from accounts.models import Contact

class NewMessageForm(forms.Form):
    msg_text = forms.CharField(widget=forms.widgets.Textarea())
    recipient = forms.ChoiceField(choices=()) # choices should be (Contact.user==current_user).contact

    def __init__(self, user):
        forms.Form.__init__(self)

        contacts = Contact.objects.filter(user=user)
        contact_choices = [(contact.id, contact.username) for contact in contacts]
        # add self. this should appear as a default contact in the database
        contact_choices += [(user.id, user.username)]
        self.fields['recipient'].choices = contact_choices
