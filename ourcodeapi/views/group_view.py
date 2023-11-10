from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ourcodeapi.models import Coder, Group
from django.contrib.auth.models import User

class GroupView(ViewSet):

    def retrieve(self, request, pk):
        group = Group.objects.get(pk = pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    def list(self, request): 
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class CoderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Coder
        fields = ('id', 'bio', 'user')

class GroupSerializer(serializers.ModelSerializer):
    creator = CoderSerializer()
    moderator = CoderSerializer()
    group_user = CoderSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'creator', 'moderator', 'group_user', 'description')
    
    