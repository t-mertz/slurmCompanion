from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout



def sitehome(request):

    if request.method == 'GET':
        if logout in request.GET:
            logout(request)
        context = {'form' : LoginForm() }

        if request.user.is_authenticated:
            context = {'username' : request.user.username}
    
    else:
        context = {}

        form = LoginForm(request.POST)

        if form.is_valid():
            uname = form.cleaned_data['input_name']
            pword = form.cleaned_data['input_password']

            user = authenticate(username=uname, password=pword)

            if user is not None:
                login(request, user)
                context.update({ 'login_failed' : False,
                                 'username' : uname 
                                 })
                
            else:
                context.update({ 'login_failed' : True })


    return render(request, 'sitehome.html', context=context)
