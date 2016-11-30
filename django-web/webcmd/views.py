from django.shortcuts import render
from django.http import HttpResponse

from .forms import CmdForm

# Create your views here.

def index(request):
    return HttpResponse("index")
    


def cmd(request):

    if request.method == 'POST':
        form = CmdForm(request.POST)

        if form.is_valid():
            cmd_string = form.cleaned_data['input_cmd']

            #form.cleaned_data['output_field'] = "response"
            context = {'cmd': cmd_string,
                       'response': "response"
                      }
        else:
            context = {}
        #return HttpResponseRedirect('/cmd/cmd')
    
    else:
        form = CmdForm()
        context = {}

    context.update({'form': form})
    

    #return HttpResponse("cmd")
    return render(request, 'webcmd/cmd.html', context=context)
