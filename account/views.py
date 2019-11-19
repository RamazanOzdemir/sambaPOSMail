from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout

from .forms import myUserCreationForm,myAuthenticationForm
from mails.models import Person

def signup_view(request):
    if request.method == 'POST':
        form= myUserCreationForm(request.POST)
        print(form. data['firstName'])
        if form.is_valid():
            # save() user dönüyor. onu login yapıyoruz
            user = form.save()
            #mailbox oluştur
           
            
            person = Person(person=user,first_name=form.data['firstName'],last_name=form.data['lastName'],personColor=form.data['color'])
            person.save()
            #LOGIN
            login(request,user)
            return redirect('mails:inbox')
    else:
        form = myUserCreationForm()
    return render(request,'account/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = myAuthenticationForm(data=request.POST)
        if form.is_valid():
            # form dan user'ı alıyorum
            user = form.get_user()
            #LOGIN
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('mails:inbox')
    else:
        form = myAuthenticationForm()
    return render(request,'account/login.html',{'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('account:login')