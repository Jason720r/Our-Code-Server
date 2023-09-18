from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ourcodeapi.models import Event, Coder

class AttendEvent(APIView):
    
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        # Ensure the current user is not the organizer
        if request.user == event.organizer.user:
            return Response({"error": "Organizer cannot attend their own event!"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user is already an attendee
        if event.attendees.filter(user=request.user).exists():
            return Response({"error": "You are already attending this event!"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the user as an attendee
        attendee = Coder.objects.get(user=request.user)
        event.attendees.add(attendee)
        
        return Response({"message": "Successfully attended the event!"}, status=status.HTTP_200_OK)
    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

    # Ensure the current user is already an attendee
        if not event.attendees.filter(user=request.user).exists():
            return Response({"error": "You are not attending this event!"}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the user as an attendee
        attendee = Coder.objects.get(user=request.user)
        event.attendees.remove(attendee)
    
        return Response({"message": "Successfully un-attended the event!"}, status=status.HTTP_200_OK)
