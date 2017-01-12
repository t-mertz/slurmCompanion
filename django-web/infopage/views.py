from django.shortcuts import render

from .models import Info

# Create your views here.

def index(request):
    info_list = Info.objects.order_by('-pub_date')

    context = {'info_list' : info_list, }

    return render(request, 'infopage/index.html', context)