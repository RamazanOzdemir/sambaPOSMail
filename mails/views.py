from django.shortcuts import render,redirect
from imbox import Imbox
from .models import Person,OutgoingEmail,IncomingEmail
from datetime import datetime
from django.template.loader import render_to_string
from . import forms
from django.core.mail import send_mail,EmailMessage,get_connection
import uuid
def inbox(request):
    user = request.user
    person = Person.objects.get(person=user)

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
       
        if date > last_message_date  :
            print(date)
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
    my_incoming = []
    all_incoming = []      
    for mail in inbox_mails:
        reply_persons = mail.reply_persons.all()
        all_incoming.append([mail,reply_persons])
        if person in reply_persons:
            my_incoming.append([mail,reply_persons])


    return render(request,'mails/inbox.html',{'inbox_mails':inbox_mails,'all_incoming':all_incoming,'my_incoming':my_incoming })
def create(request,**args):
    
    user = request.user
    person = Person.objects.get(person=user)
    
           
    
    if request.method == 'POST':
        form = forms.CreateEmail(request.POST,request.FILES)
        if form.is_valid:
            
            #save form
            if len(args)>0:
                uid = args['uid']
                incoming_mail = IncomingEmail.objects.get(uid=uid)
                incoming_mail.reply_persons.add(person)
                subject = 'Re: {}'.format(incoming_mail.subject)
                to_email = incoming_mail.from_email
                to_name = incoming_mail.from_name
                #html_content = "<div dir='ltr'>{}<div dir='rtl'>{}</div></div>".format(form.data['reply'],incoming_mail.body_html)
                html_content = "<div dir='ltr'>{}</div>".format(form.data['reply'])
                body_plain = form.data['reply']
            else:
                subject = form.data['subject']
                to_email = form.data['to_email']
                to_name = ''
                if 'to' in  form.data:
                    
                    html_content = render_to_string('mails/template_message.html', {'to':form.data['to'],'body':form.data['body'],'name':form.data['name']})
                    body_plain = form.data['to'] + form.data['body'] + form.data['name']
                else:
                    html_content = form.data['body_html']
                    body_plain = form.data['body_html']
            connection = get_connection(backend=None,fail_silently=False, username='dene6606@gmail.com', password='Kartal1903')
            email = EmailMessage(subject, html_content, 'dene6606@gmail.com',
            [to_email,],connection=connection, headers = {'Reply-To': 'dene6606@gmail.com'})
            email.content_subtype = "html"
            #email.attach_file('./assets/sambaPOS.png')
            email.send()
            outgoing = OutgoingEmail(
                uid = str(uuid.uuid4()),
                subject = subject,
                to_name = to_name,
                to_email = to_email,
                body_plain = body_plain,
                body_html = html_content,
            )
            outgoing.save()
            outgoing.reply_persons.add(person)
            #print(html_content)
            return redirect('mails:inbox')
    else:
       
        form = forms.CreateEmail()
        formTemplate = forms.CreateTenplateEmail()
    return render(request,'mails/create.html',{'form':form,'formTemplate':formTemplate})




def detail(request,uid):
    mail =  IncomingEmail.objects.filter(uid=uid)
    incoming = True
    if len(mail) == 0:
        mail =  OutgoingEmail.objects.filter(uid=uid)
        incoming = False
    
    return render(request,'mails/detail.html',{'mail':mail[0],'incoming':incoming })

def outbox(request):
    user = request.user
    person = Person.objects.get(person=user)
    outgoing = OutgoingEmail.objects.all()
    my_outgoing = []
    all_outgoing = []
    for mail in outgoing:
        reply_persons = mail.reply_persons.all()
        all_outgoing.append([mail,reply_persons])
        if person in reply_persons:
            my_outgoing.append([mail,reply_persons])
   
    
    return render(request,'mails/outbox.html',{'outgoing_mails':all_outgoing,'my_outgoing_mails':my_outgoing})

def delete(request):
    if request.method == 'POST':
        check_list_inbox = request.POST.getlist('message_checkbox_inbox')
        check_list_outbox = request.POST.getlist('message_checkbox_outbox')
        print(check_list_outbox)
        for uid in check_list_inbox: 
            print (IncomingEmail.objects.filter(uid = uid).delete())
        for uid in check_list_outbox: 
            print (OutgoingEmail.objects.filter(uid = uid).delete())
        if 'inbox' in request.POST:
            return redirect('mails:inbox')
        print(check_list_inbox)
    return redirect('mails:outbox')
