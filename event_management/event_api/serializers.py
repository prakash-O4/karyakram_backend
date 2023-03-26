
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket, BookEvent


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if(email is None):
            raise serializers.ValidationError("Email is required.")
        return super(RegisterSerializer, self).validate(data)
    
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['email'], email=validated_data['email'], password=validated_data['password'],first_name=validated_data["first_name"], last_name=validated_data["last_name"])
        user.set_password(validated_data['password'])
        return user

class TicketSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'ticket_type', 'ticket_price',)
    
    def create(self, validated_data):
        ticket = Ticket.objects.create(ticket_type=validated_data['ticket_type'], ticket_price=validated_data['ticket_price'])
        return ticket
    
    def validate(self, data):
        event = data.get('event', None)
        ticket_type = data.get('ticket_type', None)
        ticket_price = data.get('ticket_price', None)
        if Ticket.objects.filter(ticket_type=ticket_type).exists():
            raise serializers.ValidationError("A ticket with that type already exists.")
        if len(ticket_type) < 5:
            raise serializers.ValidationError("Ticket type must be at least 5 characters long.")
        return super(TicketSerialzer, self).validate(data)   

class EventSerializer(serializers.ModelSerializer):
    ticket = TicketSerialzer(read_only=True)
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'picture', 'start_date', 'end_date','ticket','address')
    
    def create(self, validated_data):
        event = Event.objects.create(name=validated_data['name'], description=validated_data['description'], picture=validated_data['picture'], start_date=validated_data['start_date'], end_date=validated_data['end_date'], ticket=validated_data['ticket'], address=validated_data['address'])
        return event
    
    def validate(self, data):
        name = data.get('name', None)
        description = data.get('description', None)
        picture = data.get('picture', None)
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        if Event.objects.filter(name=name).exists():
            raise serializers.ValidationError("An event with that name already exists.")
        if len(description) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        if len(picture) < 10:
            raise serializers.ValidationError("Picture must be at least 10 characters long.")
        return super(EventSerializer, self).validate(data)
    
    
class BookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEvent
        fields = ('id', 'user', 'event', 'ticket',)
        extra_kwargs = {'user': {'write_only': True}, 'event': {'write_only': True}, 'ticket': {'write_only': True}}
    
    def create(self, validated_data):
        book_event = BookEvent.objects.create(user=validated_data['user'], event=validated_data['event'], ticket=validated_data['ticket'])
        return book_event
    
    def validate(self, data):
        user = data.get('user', None)
        event = data.get('event', None)
        # if BookEvent.objects.filter(user=user, event=event).exists():
        #     raise serializers.ValidationError("You have already booked this event.")
        return super(BookEventSerializer, self).validate(data)