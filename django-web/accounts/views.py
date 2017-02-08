from django.shortcuts import render

from slurmui.views import get_default_context

# Create your views here.


def manage_servers(request):
    context = get_default_context(request)

    return render(request, 'accounts/server_manage.html', context)