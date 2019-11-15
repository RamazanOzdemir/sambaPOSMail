from django.contrib import admin
from .models import Person,IncomingEmail,OutgoingEmail


admin.site.register(Person)
admin.site.register(IncomingEmail)
admin.site.register(OutgoingEmail)
