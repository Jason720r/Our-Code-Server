from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ourcodeapi.models import Post, Coder
from django.contrib.auth.models import User

class PostView(ViewSet):

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def list(self, request):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    
    def create(self,request):

        poster_instance = Coder.objects.get(user=request.user)

        post = Post.objects.create(
        title = request.data["title"],
        description = request.data["description"],
        date = request.data["date"],
        poster = poster_instance
    )
        serializer = PostSerializer(post)
        return Response(serializer.data)
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status= status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.description = request.data["description"]
        post.date = request.data["date"]
        
        poster = Coder.objects.get(pk=request.data["poster"])
        post.poster = poster
        post.save()

        serializer = PostSerializer(post)
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


class PostSerializer(serializers.ModelSerializer):
    poster = CoderSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'date', 'poster') 
