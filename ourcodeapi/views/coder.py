from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ourcodeapi.models import Coder

class CoderView(ViewSet):

    def retrieve(self, request, pk):
        coder = Coder.objects.get(pk=pk)
        serializer = CoderSerializer(coder)
        return Response(serializer.data)
    
    def list(self, request):
        coder = Coder.objects.all()
        serializer = CoderSerializer(coder, many=True)
        return Response(serializer.data)
class CoderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coder
        fields = ('id','user', 'bio')