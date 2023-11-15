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
    def create(self, request):

        creator_instance = Coder.objects.get(user=request.user)

        group = Group.objects.create(
        creator = creator_instance,
        name = request.data["name"],
        description = request.data["description"]
        )
        moderator_ids = request.data.get("moderators", [])
        for moderator_id in moderator_ids:
            moderator = Coder.objects.get(pk=moderator_id)
            group.moderators.add(moderator)
        group.save()

        group_users = request.data.get("group_users", [])
        for group_user in group_users:
            group_user = Coder.objects.get(pk=group_user)
            group.group_users.add(group_user)
        group.save()
        
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        group = Group.objects.get(pk=pk)
        group.delete()
        return Response(None, status = status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):

        group = Group.objects.get(pk=pk)

        if "moderator" in request.data:
            moderator_instance = Coder.objects.get(pk=request.data["moderator"])
            group.moderator = moderator_instance

        group.name = request.data.get("name", group.name)
        group.description = request.data.get("description", group.description)

        group.save()

        serializer = GroupSerializer(group)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
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
        fields = ('id', 'name', 'creator', 'moderator', 'group_user', 'description')
    
    