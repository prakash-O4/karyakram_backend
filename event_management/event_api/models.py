from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    ticket_type = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.ticket_type

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    picture = models.CharField(max_length=300, blank=True, null=True)
    start_date = models.DateTimeField(blank=False, null=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    end_date = models.DateTimeField(blank=False, null=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    

    

class BookEvent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.event.name