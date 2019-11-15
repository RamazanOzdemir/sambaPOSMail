from django.shortcuts import render,redirect
from imbox import Imbox
from .models import Person,OutgoingEmail,IncomingEmail
from datetime import datetime
from django.template.loader import render_to_string
from . import forms
from django.core.mail import send_mail,EmailMessage,get_connection

def inbox(request):
    user = request.user
    person = Person.objects.get(person=user)
    print(person)

    imbox = Imbox('imap.gmail.com',
      username = 'dene6606@gmail.com',
      password = 'Kartal1903',
      ssl=True,
      ssl_context=None,
      starttls=False )
    
    last_message = IncomingEmail.objects.last()
    last_message_date = datetime.strptime('1990,1,1 +03:00','%Y,%m,%d %z')
    if last_message != None:
        last_message_date = last_message.date

    all_inbox_messages = imbox.messages()
   

    for uid, message in all_inbox_messages:
        d=message.date.replace('(GMT)','').strip()
        date=datetime.strptime(d,'%a, %d %b %Y %H:%M:%S %z')
        print(last_message_date)
        print(date)
        if date > last_message_date  :
            uid = uid
            subject = message.subject
            from_name = message.sent_from[0]['name']
            from_email = message.sent_from[0]['email']
            to_name = message.sent_to[0]['name']
            to_email = message.sent_to[0]['email']
            body_plain = message.body['plain'][0]
            body_html = message.body['html'][0]
            date = date
            incoming = IncomingEmail(
                uid=uid,
                subject=subject,
                from_name = from_name,
                from_email = from_email,
                to_name = to_name,
                to_email = to_email,
                body_plain = body_plain,
                body_html = body_html,
                date = date,
                )
            incoming.save()
                 
    inbox_mails = IncomingEmail.objects.order_by('date').reverse()      



    return render(request,'mails/inbox.html',{'inbox_mails':inbox_mails })
def create(request):
    if request.method == 'POST':
        form = forms.CreateEmail(request.POST,request.FILES)
        if form.is_valid:
            #save form
            print(form.data['to'])
            print(form.data['body'])
            print(form.data['name'])
            html_content = render_to_string('mails/template_message.html', {'to':form.data['to'],'body':form.data['body'],'name':form.data['name']})
            connection = get_connection(backend=None,fail_silently=False, username='dene6606@gmail.com', password='Kartal1903')
            email = EmailMessage(form.data['subject'], html_content, 'dene6606@gmail.com',
            [form.data['sent_to_email'],],connection=connection, headers = {'Reply-To': 'dene6606@gmail.com'})
            email.content_subtype = "html"
            email.attach_file('./assets/sambaPOS.png')
            email.send()
            print(html_content)
            return redirect('mails:inbox')
    else:
       
        form = forms.CreateEmail()
        formTemplate = forms.CreateTenplateEmail()
    return render(request,'mails/create.html',{'form':form,'formTemplate':formTemplate})

def detail(request,uid):
    mail =  IncomingEmail.objects.values().get(uid=uid)
    return render(request,'mails/detail.html',{'mail':mail})
