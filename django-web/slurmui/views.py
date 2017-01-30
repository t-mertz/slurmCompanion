from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, AddSshServerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sshcomm.models import UserData, RemoteServer
from sshcomm import security, comm


def get_default_context(request):
    logged_in = request.user.is_authenticated

    login_form = LoginForm() if not logged_in else None
    
    username = request.user.username if logged_in else None

    return {'logged_in': logged_in,
            'username': username,
            'form': login_form,
            }

def perform_logout(request):
    context = {}
    if request.method == 'GET':
        #print(request.GET)
        if 'logout' in request.GET:
            logout(request)
        context = {'login_form' : LoginForm(),
                    'logged_in': False }

        #if request.user.is_authenticated:
        #    context = {'username' : request.user.username}
    
    return request, context

def login_view(request):

    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))

    login_disabled = not context['logged_in']
    context.update({'login_disabled': login_disabled, })

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            uname = form.cleaned_data['input_name']
            pword = form.cleaned_data['input_password']

            user = authenticate(username=uname, password=pword)

            if user is not None:
                login(request, user)

                # get hashkey and save in session
                hashkey = security.create_key(uname, pword)
                
                # store the stringified hashkey in session
                request.session['hashkey'] = security.encode_key(hashkey)


                context.update({'login_failed' : False,
                                #'username' : uname,
                                #'logged_in': request.user.is_authenticated,
                                })

                return HttpResponseRedirect(reverse('userhome'))
                
            else:
                context.update({'login_failed' : True,
                                #'logged_in': request.user.is_authenticated,
                                })
            
            context.update(get_default_context(request))


    return render(request, 'login.html', context)

@login_required
def user_home(request, user_id=None):
    # handle logout
    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))
    
    if not context['logged_in']:
        return HttpResponseRedirect(reverse('siteindex'))
    ##

    context = get_default_context(request)

    return render(request, 'userhome.html', context)

def sitehome(request):

    if request.method == 'GET':
        #print(request.GET)
        if 'logout' in request.GET:
            logout(request)
        context = {'login_form' : LoginForm() }

        #if request.user.is_authenticated:
        #    context = {'username' : request.user.username}
    
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
                hashkey = security.create_key(uname, pword)
                
                # store the hashkey in session
                #request.session['hashkey'] = hashkey


                context.update({'login_failed' : False,
                                #'username' : uname,
                                #'logged_in': request.user.is_authenticated,
                                })
                
            else:
                context.update({'login_failed' : True,
                                #'logged_in': request.user.is_authenticated,
                                'login_form': form,
                                })
            
            context.update(get_default_context(request))


    return render(request, 'sitehome.html', context=context)


@login_required
def settingspage(request):
    
    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))
    
    if not context['logged_in']:
        return HttpResponseRedirect(reverse('siteindex'))


    context.update({
        'add_server_form': AddSshServerForm(),
    })
    return render(request, 'settings.html', context=context)

@login_required
def serversettings_addserver(request):

    # handle logout
    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))
    
    if not context['logged_in']:
        return HttpResponseRedirect(reverse('siteindex'))
    ##
    
    profile = None
    url = None
    test_status = None
    test_msg = None
    error_message = None
    server_name = None
    server_url = None
    server = None

    if (request.method == "POST"):
        form = AddSshServerForm(request.POST)
        
        form_validated = form.is_valid()

        if not form_validated and (len(form.errors.as_data()) == 1 and 'input_password' in form.errors.as_data()):
            # override password validation
            form.cleaned_data['input_password'] = request.POST['input_password']
            form_validated = True

        if form_validated:
            # get input
            server_name = form.cleaned_data['select_name']
            #url = form.cleaned_data['input_url']
            profile = form.cleaned_data['input_profile_name']
            server = RemoteServer.objects.get(server_name__exact=server_name)
            username = form.cleaned_data['input_username']
            password = form.cleaned_data['input_password']
            loc_password = form.cleaned_data['input_loc_password']
            

            # look for existing entry with that name
            if (len(UserData.objects.filter(owner__exact=request.user, profile__exact=profile))>0):
                # entry already existed
                pass
                error_message = "Profile {} already existed.".format(profile)
            else:
                # encrypt username and password
                hashkey = security.create_key(request.user.username, loc_password)
                
                # store the hashkey in session
                request.session['hashkey'] = security.encode_key(hashkey)
                

                # encrypt credentials for storage
                crypt_uname = security.encode_key(security.encrypt_Crypto(username, hashkey))
                crypt_pw = security.encode_key(security.encrypt_Crypto(password, hashkey))

                # create entry
                new_data = UserData(owner=request.user, profile=profile, server=server, user_name=crypt_uname, user_password=crypt_pw)
                new_data.save()

                # test connection?
                cdata = comm.ConnectionData(server.server_url, username, password)
                test_result = comm.test_connection_data(cdata)
                test_status = test_result.get_success()
                test_msg = test_result.get_info()

        else:
            # Form is not valid
            pass
            error_message = "Form is not valid."
            print(form.errors.as_data())
            #print("form invalid")
            #print(form)
    
    if server:
        server_name = server.server_name
        url = server.server_url
    
    context.update({'error_message': error_message,
                    'profile': profile,
                    'url': url,
                    'server_name': server_name,
                    'test_status': test_status,
                    'test_msg': test_msg,})
    
    """
    context.update({
        'add_server_form': AddSshServerForm(),
    })
    """
    return render(request, 'server_settings_red.html', context=context)

def add_user_data(userdata, loc_user, test=False):
    
    profile = userdata['profile']
    server = userdata['server']
    username = userdata['username']
    password = userdata['password']
    loc_password = userdata['loc_password']

    context = {}

    # look for existing entry with that name
    if (len(UserData.objects.filter(owner=loc_user, profile=profile))>0):
        # entry already existed
        pass
        error_message = "Profile {} already existed.".format(profile)
        context.update({'error_message': error_message})
    else:
        # encrypt username and password
        hashkey = security.create_key(loc_user.username, loc_password)

        # encrypt credentials for storage
        crypt_uname = security.encode_key(security.encrypt_Crypto(username, hashkey))
        crypt_pw = security.encode_key(security.encrypt_Crypto(password, hashkey))

        # create entry
        new_data = UserData(owner=loc_user, profile=profile, server=server, user_name=crypt_uname, user_password=crypt_pw)
        new_data.save()

        if test:
            # test connection?
            cdata = comm.ConnectionData(server.server_url, username, password)
            test_result = comm.test_connection_data(cdata)
            test_status = test_result.get_success()
            test_msg = test_result.get_info()
            
            context.update({'test_status': test_status,
            'test_msg': test_msg})
    
    return context