from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class Person (models.Model):
    objects = models.Manager()
    COLOR_CHOICES = [
        ('#e53935', 'Kırmızı'),
        ('#1976d2', 'Mavi'),
        ('#00796b', 'Yeşil'),
        ('#ffeb3b', 'Sarı'),
        ('#f4511e', 'Turuncu'),
        ('#546e7a', 'Gri'),
        ('#5e35b1', 'Mor'),
    ]
    uid = models.CharField(max_length=50,default=uuid.uuid4())
    person = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50,default='')
    personColor = models.CharField(max_length=15,choices=COLOR_CHOICES,default='#1976d2',)
    is_Super_Person = models.BooleanField(default=False)
    wait_to_reply = models.ManyToManyField('IncomingEmail', related_name='incomingemails')

    def __str__(self):
        self.full_name=("{} {}".format(self.first_name, self.last_name))
        return self.full_name
    def avatar(self):        
        return ("{} {}".format(self.first_name[0], self.last_name[0])).upper()
  
class IncomingEmail(models.Model):
    objects = models.Manager()
    uid = models.CharField(max_length=50)
    subject = models.CharField(max_length=250)
    from_name = models.CharField(max_length=100)
    from_email = models.EmailField(max_length=100)
    to_name = models.CharField(max_length=100)
    to_email = models.CharField(max_length=250)
    body_plain = models.TextField()
    body_html = models.TextField()
    date = models.DateTimeField(auto_now=False)
    reply_persons = models.ManyToManyField('Person', related_name='incomingemails')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.subject

class OutgoingEmail(models.Model):
    objects = models.Manager()
    uid = models.CharField(max_length=50)
    subject = models.CharField(max_length=250)
    from_name = models.CharField(max_length=100)
    from_email = models.EmailField(max_length=100)
    to_name = models.CharField(max_length=100)
    to_email = models.CharField(max_length=250)
    body_plain = models.TextField()
    body_html = models.TextField()
    date = models.DateTimeField(auto_now=True)
    reply_persons = models.ManyToManyField('Person', related_name='outgoingemails')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.subject

class LastMessage(models.Model):
    objects = models.Manager()
    date = models.DateTimeField(default=datetime(1990,1,1 ))

    def __str__(self):
        return str(self.date)