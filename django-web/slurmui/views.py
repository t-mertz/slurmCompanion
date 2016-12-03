from django.shortcuts import render
from django.http import HttpResponse


def sitehome(request):

    return render(request, 'sitehome.html')
