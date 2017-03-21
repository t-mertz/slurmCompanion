from django.shortcuts import render

from slurmui.views import get_default_context

# Create your views here.

def messenger(request):
    context = get_default_context(request)

    return render(request, 'messenger.html', context=context)

def messenger_session(request, user_id):
    """Messenger session with a paticular user.

    This might be replaced by a consumer.
    """
    pass
