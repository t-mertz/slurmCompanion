from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import CmdForm
from .cmdtext import CmdText, Command, Response
from slurmui.views import get_default_context, perform_logout
from sshcomm.models import UserData

# Create your views here.

PROMPT_SYMBOL = "?>"

def index(request):
    return HttpResponse("index")
    


def clear_cmd(request):

    
    try:
        del request.session['command_list']
        del request.session['response_list']
    except:
        pass
    

    form = CmdForm()
    context = {'cmd_res_list': [[], []],
               'form': form
              }
    
    return render(request, 'webcmd/cmd.html', context=context)

@login_required
def cmd(request, server_name=None):
    
    # determine login status to handle the login/logout forms
    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))

    login_disabled = not context['logged_in']
    context.update({'login_disabled': login_disabled, })
    ##
    
    request.session.set_expiry(0)

    if request.method == 'GET':
        if 'clear-shell' in request.GET:
            try:
                del request.session['command_list']
                del request.session['response_list']
            except KeyError:
                pass
            request.session.flush()
            cmd_res_list = [[], []]
            context.update({'cmd_res_list': request.session['command_list']})#cmd_res_list}
        else:
            context.update({'cmd_res_list': [[], []]})
        
        form = CmdForm()

    elif request.method == 'POST':
        form = CmdForm(request.POST)

        if form.is_valid():
            
            cmd_string = form.cleaned_data['input_cmd']
            if 'command_list' not in request.session:
                request.session['command_list'] = []
            cur_cmd = Command("user@192.168.178.112:~$" + PROMPT_SYMBOL + cmd_string)
            request.session['command_list'].append(cur_cmd[:])
            cur_cind = len(request.session['command_list'])

            # This is just experimental and will be replaced
            try:
                import sshcomm.comm as comm
                cdata = comm.ConnectionData("192.168.178.112", "user", " ")
                response_string = comm.run_command(cdata, cmd_string)
            except Exception as e:
                response_string = "[backend failed: {}] response to ".format(e) + cmd_string
            if 'response_list' not in request.session:
                request.session['response_list'] = []
            cur_res = Response(response_string, cur_cind)
            request.session['response_list'].append(cur_res[:])
            cur_rind = len(request.session['response_list'])

            cmd_res_list = []
            for c,r in zip(request.session['command_list'], request.session['response_list']):
                cmd_res_list.append([c, r])

            # update response
            #request.session['command_list'][-1].response = cur_rind

            cmd_string = PROMPT_SYMBOL + cmd_string
            response_string = PROMPT_SYMBOL + response_string

            # TEST
            #out_string = ""
            #for c in request.session['command_list']:
            #    out_string += c + "\n"

            #form.cleaned_data['output_field'] = "response"
            context.update({'cmd': request.session['command_list'],
                       'response': response_string,
                       'command_list': request.session['command_list'],
                       'response_list': request.session['response_list'],
                       'cmd_res_list': cmd_res_list
                      })
            
        else:
            #context = {}
            pass
        #return HttpResponseRedirect('/cmd/cmd')
    
    else:
        form = CmdForm()
        #context = {}
    
    context.update({'form': form})
    

    #return HttpResponse("cmd")
    #return render(request, 'webcmd/cmd.html', context=context)
    return render(request, 'webcmd/cmd_ws.html', context=context)

def get_paragraph_string(string):
    out = "<p>"
    out += string
    out += "</p>"

    return out

def cmd_selection(request, context=None):
    """
    Offers all the user's profile for selection.
    """
    # determine login status to handle the login/logout forms
    context = {}

    if request.method == 'GET':
        request, context = perform_logout(request)

    context.update(get_default_context(request))

    login_disabled = not context['logged_in']
    context.update({'login_disabled': login_disabled, })
    ##

    server_list = UserData.objects.filter(owner=request.user)

    context.update({'server_list', server_list})

    return render(request, 'cmd_select.html', context=context)