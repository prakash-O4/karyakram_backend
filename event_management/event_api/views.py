from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Event,  BookEvent
from .serializers import RegisterSerializer, BookEventSerializer, EventSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your views here.
 

class RegisterView (APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValidationError, Exception) as e:
            #print(e['NON_FIELD_ERRORS_KEY'])
            #serializer.errors['NON_FIELD_ERRORS_KEY'] = e
            errorMessgae = serializer.errors['non_field_errors']
            return Response({'error': errorMessgae}, status=status.HTTP_400_BAD_REQUEST)
        
# book event
class BookEventView (APIView):
    serializer_class = EventSerializer
    #permission_classes = (IsAuthenticated)

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.query_params.get('user', None)
            current_user = User.objects.get(id=user)
            book_event = BookEvent.objects.filter(user=current_user)
            # get list of events from book_event
            print(book_event)
            event_list = []
            for event in book_event:
                events = Event.objects.get(id=event.event.id)
                event_list.append(events)
            serializer = self.serializer_class(event_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValidationError, Exception) as e:
            print(e)
            return Response({'error': "Couldn't fetch your booked events."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            isValid = serializer.is_valid(raise_exception=True)
            if(isValid):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            #print(e['NON_FIELD_ERRORS_KEY'])
            #serializer.errors['NON_FIELD_ERRORS_KEY'] = e
            errorMessgae = serializer.errors['non_field_errors']
            return Response({'error': errorMessgae}, status=status.HTTP_400_BAD_REQUEST)
    

class GetEventList(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        # filter event with name 
        # filter with the start_date and end_date
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        address = self.request.query_params.get('address', None)
        if address is not None:
            events = Event.objects.filter(address__icontains=address)
        elif start_date is not None and end_date is not None:
            events = Event.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
        elif start_date is not None:
            events = Event.objects.filter(start_date__gte=start_date)
        elif end_date is not None:
            events = Event.objects.filter(end_date__lte=end_date)
        else:
            events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
      
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request},)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user_id': user.pk,
                'email': user.email,
                'token': token.key,
            }, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(data={"error": "Invalid Credentials."}, status=status.HTTP_404_NOT_FOUND)
        
