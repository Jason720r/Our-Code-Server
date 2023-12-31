from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from ourcodeapi.models import Category

class CategoryView(ViewSet):

    def retrieve(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


    def list(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    
    def create(self, request):

        category = Category.objects.create(
        label=request.data["label"],

    )
        serializer = CategorySerializer(category)
        return Response(serializer.data)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'label')