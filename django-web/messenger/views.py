from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from slurmui.views import get_default_context
from .models import get_recent_messages
from .forms import NewMessageForm
from accounts.models import Contact

# Create your views here.

@login_required
def messenger(request):
    context = get_default_context(request)

    message_display_days = 7
    recent_messages = get_recent_messages(request.user, days=message_display_days)

    context.update({'recent_messages': recent_messages,
                    'message_display_days': message_display_days})

    return render(request, 'messenger/messenger.html', context=context)

@login_required
def compose(request):
    context = get_default_context(request)

    if request.method == "GET":
        #contacts = Contact.objects.filter(user=request.user)
        #contact_choices = [contact.username for contact in contacts]
        # add self. this should appear as a default contact in the database
        #contact_choices += [request.user.username]

        #print(contact_choices)

        message_form = NewMessageForm(user=request.user)
        context.update({'message_form': message_form})
    else:
        return HttpResponseRedirect("messenger")

    return render(request, 'messenger/compose.html', context=context)

def messenger_session(request, user_id):
    """Messenger session with a paticular user.

    This might be replaced by a consumer.
    """
    pass

