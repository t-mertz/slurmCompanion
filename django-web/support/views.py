from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from slurmui.views import get_default_context, perform_logout


# Create your views here.

@login_required
def index(request):

    # login/logout status
    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))

    login_disabled = not context['logged_in']
    context.update({'login_disabled': login_disabled, })
    ##


    return render(request, 'support/index.html', context=context)