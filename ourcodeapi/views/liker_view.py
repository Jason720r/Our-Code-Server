from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ourcodeapi.models import Post, Coder

class PostLiker(APIView):

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.likers.filter(user=request.user).exists():
            return Response({"error": "You have already liked this post you goober!"}, status=status.HTTP_400_BAD_REQUEST)
        
        liker = Coder.objects.get(user=request.user)
        post.likers.add(liker)

        return Response({"message": "You liked this post!"}, status=status.HTTP_200_OK)
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        liker = Coder.objects.get(user=request.user)
        post.likers.remove(liker)

        return Response({"message": "Un-liked post ;("}, status=status.HTTP_400_BAD_REQUEST)