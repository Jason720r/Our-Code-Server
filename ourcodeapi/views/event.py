from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ourcodeapi.models import Event, Coder, Category
from django.contrib.auth.models import User

class EventView(ViewSet):

    def retrieve(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def list(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
    
    def create(self, request):

        organizer_instance = Coder.objects.get(user=request.user)
        type_instance = Category.objects.get(pk=request.data["type"])

        event = Event.objects.create(
        organizer = organizer_instance,
        number_of_people = request.data["number_of_people"],
        description = request.data["description"],
        location = request.data["location"],
        type = type_instance,
        date = request.data["date"]
    )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status= status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class CoderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Coder
        fields = ('id', 'bio', 'user')
    
class EventSerializer(serializers.ModelSerializer):
    organizer = CoderSerializer()

    class Meta:
        model = Event
        fields = ('id', 'organizer', 'number_of_people', 'description', 'location', 'type', 'date')