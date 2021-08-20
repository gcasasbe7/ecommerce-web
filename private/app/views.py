from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategoryNameSerializer, CategorySerializer, ProductSerializer
from .models import *

class AllProductsView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class ProductDetail(APIView):
    def get_object(self, product_slug, category_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, product_slug, category_slug, format=None):
        product = self.get_object(product_slug, category_slug)
        serializer = ProductSerializer(product)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class AllCategoriesView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class ShopView(APIView):
    def get(self, request, format=None):
        # TODO: RETURN ALL THE SHOP DATA
        # CUSTOM SERIALIZER FOR SHOP?
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})
