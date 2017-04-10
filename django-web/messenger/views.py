from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from slurmui.views import get_default_context
from .models import get_recent_messages
from .forms import NewMessageForm

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
        message_form = NewMessageForm()
        context.update({'message_form': message_form})
    else:
        return HttpResponseRedirect("messenger")

    return render(request, 'messenger/compose.html', context=context)

def messenger_session(request, user_id):
    """Messenger session with a paticular user.

    This might be replaced by a consumer.
    """
    pass

