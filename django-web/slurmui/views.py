from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm


def sitehome(request):

    context = {'form' : LoginForm() }

    return render(request, 'sitehome.html', context=context)
