from django import forms

class CmdForm(forms.Form):
    input_cmd = forms.CharField(label='Enter Command', required=False)
    #output_field = forms.CharField(widget=forms.Textarea, required=False)

    """
    def __init__(self, string=None):
        forms.Form.__init__(self)
        if (string is not None):
            self.cleaned_data['input_command'] = string
    """