from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, AddSshServerForm
from django.contrib.auth import authenticate, login, logout
from sshcomm.models import UserData, RemoteServer
from sshcomm import security



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

                # get hashkey and save in session
                hashkey = security.create_key(uname.encode('utf-8'), pword.encode('utf-8'))
                
                # store the hashkey in session
                #request.session['hashkey'] = hashkey


                context.update({ 'login_failed' : False,
                                 'username' : uname 
                                 })
                
            else:
                context.update({ 'login_failed' : True })


    return render(request, 'sitehome.html', context=context)


def settingspage(request):

    context = {
        'add_server_form': AddSshServerForm(),
    }
    return render(request, 'settings.html', context=context)

def serversettings_addserver(request):

    if (request.method == "POST"):
        form = AddSshServerForm(request.POST)

        if form.is_valid():
            # get input
            name = form.cleaned_data['select_name']
            #url = form.cleaned_data['input_url']
            server = form.cleaned_data['input_server']
            username = form.cleaned_data['input_username']
            password = form.cleaned_data['input_password']
            loc_password = form.cleaned_data['input_loc_password']
            

            # look for existing entry with that name
            if (UserData.objects.get(owner__exact=request.user, server__exact=server)):
                # entry already existed
                pass
            else:
                # encrypt username and password
                hashkey = security.create_key(request.user.username, loc_password)
                
                # store the hashkey in session
                request.session['hashkey'] = hashkey
                
                # encrypt credentials for storage
                crypt_uname = security.encrypt(hashkey, username)
                crypt_pw = security.encrypt(hashkey, password)

                # create entry
                new_data = UserData(owner=request.user, server=server, user_name=crypt_uname, user_password=crypt_pw)

                # test connection?
                pass

        else:
            # Form is not valid
            pass
        
    context = {
        'add_server_form': AddSshServerForm(),
    }
    return render(request, 'settings.html', context=context)
