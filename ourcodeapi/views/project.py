from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ourcodeapi.models import Project, Coder

class ProjectView(ViewSet):

    def retrieve(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def list(self, request):
        user_id = request.query_params.get('user_id', None)
        if user_id:
            projects = Project.objects.filter(creator__user__id=user_id)
        else:
            projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    
    def create(self, request):

        creator_instance = Coder.objects.get(user=request.user)

        project = Project.objects.create(
        title = request.data["title"],
        description = request.data["description"],
        url = request.data["url"],
        creator = creator_instance
    )
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        project = Project.objects.get(pk=pk)
        project.delete()
        return Response(None, status= status.HTTP_204_NO_CONTENT)
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        depth = 1
        fields = ('id', 'title', 'description', 'url', 'creator')