from django import forms

class CmdForm(forms.Form):
    input_cmd = forms.CharField(label='Enter Command')
    #output_field = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, string):
        self.cleaned_data['input_command'] = string