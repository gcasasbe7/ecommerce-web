from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CategoryShopListSerializer, CategorySerializer, ProductSerializer
from .models import *

class AllProductsView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class ShopProductDetail(APIView):
    def get_object(self, product_slug, category_slug):
        try:
            return Product.objects.filter(main_category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, product_slug, category_slug, format=None):
        product = self.get_object(product_slug, category_slug)
        serializer = ProductSerializer(product)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategoryShopListSerializer(categories, many=True)
            
        if serializer.is_valid:
            return Response(serializer.data)
        else: 
            return Response({'message': "Serializer not valid"})

class ShopView(APIView):
    def get(self, request, format=None):
        # Fetch all the shop categories
        categories = Category.objects.all()
        
        # Validate the data
        categories_serializer = CategoryShopListSerializer(categories, many=True)
                
        if categories_serializer.is_valid:
            return Response({
                    "categories": categories_serializer.data,
                })
        else: 
            return Response({'message': "Serializer not valid"})

class ShopCategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        all_categories = Category.objects.all()

        serializer = CategorySerializer(category)
        all_categories_serializer = CategoryShopListSerializer(all_categories, many=True)
            
        if serializer.is_valid:
            return Response({
                'category_detail': serializer.data,
                'all_categories': all_categories_serializer.data
                })
        else: 
            return Response({'message': "Serializer not valid"})


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    print("asdjhflakjsdhflkjasdhf")
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)

        if serializer.is_valid:
            return Response(serializer.data)

    return Response({"products":[]})