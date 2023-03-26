from django.contrib import admin

# Register your models here.

from .models import Event, Ticket, BookEvent

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(BookEvent)
