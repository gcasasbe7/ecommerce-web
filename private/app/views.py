from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import *

class AllProductsView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})
