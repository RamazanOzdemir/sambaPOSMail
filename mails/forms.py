from django import forms
from . import models

class CreateEmail(forms.ModelForm):
    class Meta:
        model = models.OutgoingEmail
        fields = ['subject','to_email','body_html']
    def __init__(self, *args, **kwargs):
        super(CreateEmail, self).__init__(*args, **kwargs)
        self.fields['body_html'].label =""
        for field in iter(self.fields):
            if field == 'body_html':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control col-12 mb-3'
            })
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control col-10 mb-3'
                })
            

class CreateTenplateEmail(forms.ModelForm):
    class Meta:
        model = models.OutgoingEmail
        fields = ['subject','to_email']
    def __init__(self, *args, **kwargs):
        super(CreateTenplateEmail, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
            'class': 'form-control col-10 mb-3'
            })