from django.urls import path,re_path
from . import views

app_name = 'mails'
urlpatterns = [
    path('inbox/',views.inbox, name='inbox' ),
    path('outbox/',views.outbox, name='outbox' ),
    path('create/',views.create, name='create' ),
    path('delete/',views.delete, name='delete' ),
    path('delete/<str:back>/', views.delete, name='delete'),
    path('forward/',views.forward, name='forward' ),
    path('ajax_new_message/',views.new_message, name='new_message' ),
    #path('send-mail',views.sendMail, name='sendMail' ),
    re_path(r"detail-mail/(?P<uid>[\w '-]+)/(?P<reply>[\w']+)/$",views.detail, name='detailMail' ),
    re_path(r"create/(?P<uid>[\w']+)/(?P<reply>[\w']+)/$",views.create, name='create' ),
    
]