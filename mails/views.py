from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from imbox import Imbox
from .models import Person,OutgoingEmail,IncomingEmail,LastMessage
from datetime import datetime
from django.template.loader import render_to_string
from . import forms
from django.core.mail import send_mail,EmailMessage,get_connection
import uuid
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json
@login_required(login_url='/account/login/')
def inbox(request):
    user = request.user 
    all_persons = Person.objects.all()
    person = all_persons.get(person=user)
    wait_to_reply = person.wait_to_reply.order_by('-date').all()
    imbox = Imbox('imap.gmail.com',
      username = 'dene6606@gmail.com',
      password = 'Kartal1903',
      ssl=True,
      ssl_context=None,
      starttls=False )
    
    last_message = IncomingEmail.objects.first()
    ll=LastMessage.objects.all()[0]
    
    if last_message != None:
        ll.date = last_message.date
        ll.save()
    last_message_date =ll.date

    all_inbox_messages = imbox.messages()
 

    for uid, message in all_inbox_messages:
        d=message.date.replace('(GMT)','').strip()
        date=datetime.strptime(d,'%a, %d %b %Y %H:%M:%S %z')
        if date > last_message_date  :
            print(date)
            #uid = message.message_id.replace('<','').replace('@mail.gmail.com>','')
            subject = message.subject
            from_name = message.sent_from[0]['name']
            from_email = message.sent_from[0]['email']
            to_name = message.sent_to[0]['name']
            to_email = message.sent_to[0]['email']
            body_plain = message.body['plain'][0]
            body_html = message.body['html'][0]
            date = date
            incoming = IncomingEmail(
                uid= uid,
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
                 
    inbox_mails = IncomingEmail.objects.all()

    my_incoming = []
    all_incoming = []      
    for mail in inbox_mails:
        reply_persons = mail.reply_persons.all()
        all_incoming.append([mail,reply_persons])
        if person in reply_persons:
            my_incoming.append([mail,reply_persons])

    inbox_mails= serializers.serialize('json',inbox_mails)
    return render(request,'mails/inbox.html',
    {'inbx_mails':inbox_mails,'all_incoming':all_incoming,'my_incoming':my_incoming,
    'all_persons':all_persons,'wait_to_reply':wait_to_reply,'is_super_person':person.is_Super_Person })

def new_message(request):
    user = request.user 
    all_persons = Person.objects.all()
    person = all_persons.get(person=user)
    imbox = Imbox('imap.gmail.com',
      username = 'dene6606@gmail.com',
      password = 'Kartal1903',
      ssl=True,
      ssl_context=None,
      starttls=False )

    last_message = IncomingEmail.objects.first()
    ll=LastMessage.objects.all()[0]
    
    if last_message != None:
        ll.date = last_message.date
        ll.save()
    last_message_date =ll.date

    all_inbox_messages = imbox.messages()

    liste = []

    for uid, message in all_inbox_messages:
        d=message.date.replace('(GMT)','').strip()
        date=datetime.strptime(d,'%a, %d %b %Y %H:%M:%S %z')
        print('##############################################3')

        if date > last_message_date  :
            print(date)
            #uid = message.message_id.replace('<','').replace('@mail.gmail.com>','')
            subject = message.subject
            from_name = message.sent_from[0]['name']
            from_email = message.sent_from[0]['email']
            to_name = message.sent_to[0]['name']
            to_email = message.sent_to[0]['email']
            body_plain = message.body['plain'][0]
            body_html = message.body['html'][0]
            date = date
            incoming = IncomingEmail(
                uid= uid,
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

    new_coming_message = IncomingEmail.objects.filter(date__gt=last_message_date ) 
    reply_array = []
    #my_incoming = []
    #all_incoming = []      
    for mail in new_coming_message:
        reply_persons = mail.reply_persons.all()
        reply_p= serializers.serialize('json',reply_persons)
        reply_array.append(reply_p)
        #if person in reply_persons:
        #    my_incoming.append([mail,reply_persons])
        #all_incoming.append([mail,reply_persons])



    new_msg= serializers.serialize('json',new_coming_message)
    print('************************')
    print(new_coming_message)
    print('************************')
    reply_json = json.dumps(reply_array)
    data = {'reply':reply_json,'new_msg':new_msg}
    return JsonResponse(data)


@login_required(login_url='/account/login/')
def create(request,**args):
    
    user = request.user
    person = Person.objects.get(person=user)
    
    if request.method == 'POST':
        form = forms.CreateEmail(request.POST,request.FILES)
        if form.is_valid:
            print(form)
            #save form
            if len(args)>0:
                reply = args['reply']
                uid = args['uid']
                print(uid)
                incoming_mail = IncomingEmail.objects.get(uid=uid)
                incoming_mail.reply_persons.add(person)
                subject = 'Re: {}'.format(incoming_mail.subject)
                emails = incoming_mail.from_email
                to_emails = [emails]
                to_name = incoming_mail.from_name
                #html_content = "<div dir='ltr'>{}<div dir='rtl'>{}</div></div>".format(form.data['reply'],incoming_mail.body_html)
                html_content = "<div dir='ltr'>{}</div>".format(form.data['reply'])
                body_plain = form.data['reply']
                if reply == 'reply':
                    person.wait_to_reply.remove(incoming_mail)
            else:
                subject = form.data['subject']
                emails = form.data['to_email']
                to_emails = emails.split(';')
                to_name = ''
                if 'to' in  form.data:
                    
                    html_content = render_to_string('mails/template_message.html', {'to':form.data['to'],'body':form.data['body'],'name':form.data['name'],'dept':form.data['dept']})
                    body_plain = form.data['to'] + form.data['body'] + form.data['name'] + form.data['dept']
                else:
                    html_content = form.data['body_html']
                    body_plain = form.data['body_html']
            connection = get_connection(backend=None,fail_silently=False, username='dene6606@gmail.com', password='Kartal1903')
            email = EmailMessage(subject, html_content, 'dene6606@gmail.com',
            to_emails,connection=connection, headers = {'Reply-To': 'dene6606@gmail.com'})
            email.content_subtype = "html"
            #email.attach_file('./assets/sambaPOS.png')
            email.send()
            outgoing = OutgoingEmail(
                uid = str(uuid.uuid4()),
                subject = subject,
                to_name = to_name,
                to_email = emails,
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



@login_required(login_url='/account/login/')
def detail(request,uid,reply):
    mail =  IncomingEmail.objects.filter(uid=uid)
    incoming = True
    if len(mail) == 0:
        mail =  OutgoingEmail.objects.filter(uid=uid)
        incoming = False
    
    return render(request,'mails/detail.html',{'mail':mail[0],'incoming':incoming ,'reply':reply})

@login_required(login_url='/account/login/')
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
        if 'forward' in request.POST:
            for uid in check_list_inbox: 
                IncomingEmail.objects.filter(uid = uid).delete()
        else:
            for uid in check_list_inbox: 
                IncomingEmail.objects.filter(uid = uid).delete()
            for uid in check_list_outbox: 
                OutgoingEmail.objects.filter(uid = uid).delete()
            if 'outbox' in request.POST:
                return redirect('mails:outbox')
            print(check_list_inbox)
    return redirect('mails:inbox')

def forward(request):
    if request.method == 'POST':
        check_list_person = request.POST.getlist('person_checkbox')
        check_list_message = request.POST.getlist('message_checkbox')
        persons = Person.objects.all()
        messages = IncomingEmail.objects.all()
        for person_uid in check_list_person:
            person = persons.get(uid=person_uid)
            for message_uid in check_list_message:
                person.wait_to_reply.add(messages.get(uid=message_uid))
            
        print('********************************')
        print(check_list_person)
        print(check_list_message)
        print('***********************************')
        return redirect('mails:inbox')
