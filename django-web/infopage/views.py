from django.shortcuts import render

from .models import Info
from slurmui.views import get_default_context, perform_logout

# Create your views here.

def index(request):

    request, context = perform_logout(request)

    info_list = Info.objects.order_by('-pub_date')

    context.update(get_default_context(request))

    context.update({'info_list' : info_list, })

    return render(request, 'infopage/index.html', context)