from django.urls import path,re_path
from . import views
app_name = 'account'
urlpatterns = [
    path('signup',views.signup_view,name='signup'),
    re_path(r'^login/$',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    
]