from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ourcodeapi.models import Event

class EventView(ViewSet):

    def retrieve(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def list(self, request):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        depth = 1
        fields = ('id', 'organizer', 'number_of_people', 'description', 'location', 'type', 'date')