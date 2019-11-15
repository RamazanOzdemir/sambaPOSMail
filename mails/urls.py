from django.urls import path,re_path
from . import views

app_name = 'mails'
urlpatterns = [
    path('inbox/',views.inbox, name='inbox' ),
    path('outbox/',views.outbox, name='outbox' ),
    path('create/',views.create, name='create' ),
    #path('send-mail',views.sendMail, name='sendMail' ),
    re_path(r"detail-mail/(?P<uid>[\w']+)",views.detail, name='detailMail' ),
    #re_path(r"reply-mail/(?P<uid>[\w']+)",views.replyMail, name='reply' ),
    
]