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
        name = request.data["name"],
        number_of_people = request.data["number_of_people"],
        description = request.data["description"],
        location = request.data["location"],
        type = type_instance,
        date = request.data["date"]
    )
        attendee_ids = request.data.get("attendees", [])
        for attendee_id in attendee_ids:
            attendee = Coder.objects.get(pk=attendee_id)
            event.attendees.add(attendee)
        event.save()

        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status= status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk=None):

    # Retrieve the event instance
        event = Event.objects.get(pk=pk)

    # Use the existing organizer or find a new one based on the request data
        if "organizer" in request.data:
            organizer_instance = Coder.objects.get(pk=request.data["organizer"])
            event.organizer = organizer_instance

    # Use the existing category or find a new one based on the request data
        if "type" in request.data:
            type_instance = Category.objects.get(pk=request.data["type"])
            event.type = type_instance

    # Update other event attributes
        event.name = request.data.get("name", event.name)
        event.number_of_people = request.data.get("number_of_people", event.number_of_people)
        event.description = request.data.get("description", event.description)
        event.location = request.data.get("location", event.location)
        event.date = request.data.get("date", event.date)

    # Save the updated event
        event.save()

    # Serialize and return the updated event
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class CoderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Coder
        fields = ('id', 'bio', 'user')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
    
class EventSerializer(serializers.ModelSerializer):
    organizer = CoderSerializer()
    type = CategorySerializer()
    attendees = CoderSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'organizer', 'number_of_people', 'description', 'location', 'type', 'date', 'name', 'attendees')