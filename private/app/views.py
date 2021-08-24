from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (status, generics)
from rest_framework.decorators import api_view
from .serializers import CategoryShopListSerializer, CategorySerializer, ProductSerializer, RegisterSerializer
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from .email_manager import EmailManager
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

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

class RegisterView(generics.GenericAPIView):

    def post(self, request):
        user = request.data
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # Fetch the current User Model Object
        user = User.objects.get(email=user_data['email'])

        # Retrieve the access token for the user
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relative_link = reverse('verify-email')
        absolute_url = f'http://{current_site}{relative_link}?token={str(token)}'

        email_body = f'Hello ${user.name}. Thanks for signing up with us, please press the link below to verify your account. \n{absolute_url}'
        email_subject = f'{user.name}, verify your account for iPadel'
        email_data = {
            'to': user.email,
            'body': email_body,
            'subject': email_subject
        }
        EmailManager.sendEmail(email_data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass


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