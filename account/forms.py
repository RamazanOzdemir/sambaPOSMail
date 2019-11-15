from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User 
from django import forms
from mails.models import Person

class myUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control mb-0'
        self.fields['username'].label ="Kullanıcı Adı"
        self.fields['username'].help_text ="<small>30 karakterden az, Harf, sayı ve '@/./+/-/_' içerebilir.</small>"
        self.fields['password1'].widget.attrs['class'] = 'form-control mb-0'
        self.fields['password1'].label ="Şifre"
        self.fields['password1'].help_text ="<small><ul><li>Şifreniz minimum sekiz karekter olmalı</li><li>Harf içermelidir</li></ul></small>"
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label ="Şifre Tekrarı"
        self.fields['password2'].help_text ="<small>Kontrol için şifrenizi tekrar giriniz</small>"

class myAuthenticationForm(AuthenticationForm):
    class Meta:
        model=User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(myAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control mb-0'
        self.fields['username'].label ="Kullanıcı Adı"
        self.fields['username'].error_messages={'invalid':'Lütfen kullanıcı adınızı ve şifrenizi kontrol edin!'}
        self.fields['password'].widget.attrs['class'] = 'form-control mb-0'
        self.fields['password'].label ="Şifre"
        self.fields['password'].error_messages={'invalid':'Lütfen kullanıcı adınızı ve şifrenizi kontrol edin!'}

#class createPersonForm(forms.ModelForm):
#    class Meta:
#        model=Person
#        fields = ('username', 'password')

#    def __init__(self, *args, **kwargs):
#        super(createPersonForm, self).__init__(*args, **kwargs)
#        self.fields['username'].widget.attrs['class'] = 'form-control mb-0'
#        self.fields['username'].label ="Kullanıcı Adı"
#        self.fields['username'].error_messages={'invalid':'Lütfen kullanıcı adınızı ve şifrenizi kontrol edin!'}
#        self.fields['password'].widget.attrs['class'] = 'form-control mb-0'
#        self.fields['password'].label ="Şifre"
#        self.fields['password'].error_messages={'invalid':'Lütfen kullanıcı adınızı ve şifrenizi kontrol edin!'}
        