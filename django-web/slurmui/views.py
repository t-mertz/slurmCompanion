from django.shortcuts import render
from django import HTTPResponse

from .forms import CmdForm

def cmd(request):

    if request.method == 'POST':
        form = CmdForm(request.POST)

        if form.is_valid():

            return HttpResponseRedirect('/cmd/')
    
    else:
        form = CmdForm()

    return render(request, 'cmd.html', {'form': form})
