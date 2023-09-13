from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from ourcodeapi.models import Coder
from django.contrib.auth.models import User

class CoderView(ViewSet):

    def retrieve(self, request, pk):
        coder = Coder.objects.get(pk=pk)
        serializer = CoderSerializer(coder)
        return Response(serializer.data)
    
    def list(self, request):
        coder = Coder.objects.all()
        serializer = CoderSerializer(coder, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk):

        coder = get_object_or_404(Coder, pk=pk)

        user_data = request.data.get('user', {})
      

        for field, value in user_data.items():
            setattr(coder.user, field, value)
        coder.user.save()
    
        coder.bio = request.data["bio", coder.bio]
        coder.save()

        serializer = CoderSerializer(coder)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
    
class CoderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coder
        depth = 1
        fields = ('id','user', 'bio')