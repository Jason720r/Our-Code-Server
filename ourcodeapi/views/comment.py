from rest_framework import status, serializers
from ourcodeapi.models import Comment, Post, Coder
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class CommentView(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for all comments or for comments of a specific post"""
        post_id = request.query_params.get('post', None)
        if post_id:
            comments = Comment.objects.filter(post__id=post_id)
        else:
            comments = Comment.objects.all()
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""
        post = Post.objects.get(pk=request.data['post'])

        # Assuming the Coder model is related to the user model via a OneToOneField or ForeignKey
        author_instance = Coder.objects.get(user=request.user)

        comment = Comment.objects.create(
            post=post,
            author=author_instance,
            text=request.data['text']
        )
        
        # Optionally, directly approve the comment or have a moderation system
        comment.approved_comment = True
        comment.save()

        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for a comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            comment.text = request.data['text']
            
            # Assuming you want to allow updates to the approval status from the request
            if 'approved_comment' in request.data:
                comment.approved_comment = request.data['approved_comment']

            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)
class CoderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coder
        fields = ('user', 'bio')       

class CommentSerializer(serializers.ModelSerializer):
        author = CoderSerializer()

        class Meta:
            model = Comment
            fields = ('id', 'text', 'post', 'author', 'created_date', 'approved_comment')