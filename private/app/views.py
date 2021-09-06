from django.db.models import Q
from rest_framework.views import APIView
from .managers.response_manager import ResponseManager
from rest_framework import (status, generics)
from rest_framework.decorators import api_view
from .serializers import CategoryShopListSerializer, CategorySerializer, ProductSerializer, RegisterSerializer, LoginSerializer
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .managers.email_manager import EmailManager
from .managers.highlight_manager import HighlightManager
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

# Product detail shop view
class ShopProductDetail(APIView):
    def get_object(self, product_slug, category_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_slug, category_slug, format=None):
        product = self.get_object(product_slug, category_slug)

        if product:
            serializer = ProductSerializer(product)
                
            if serializer.is_valid:
                return ResponseManager.build_successful_response({
                    'product': serializer.data
                    })
            else: 
                return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "There has been an issue with the product you are trying to view. Please try again later.")

        return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, "Product not found. Please try again later.")

# Categories list including Hihglighted section if valid
class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategoryShopListSerializer(categories, many=True)

        if serializer.is_valid:
            return ResponseManager.build_successful_response({
                'categories': serializer.data,
                'highlight': HighlightManager.getHighlightCategory() if HighlightManager.shouldDisplayHighlights() else ''
            })
        else: 
            return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "There has been an issue with some category you are trying to view. Please try again later.")

# Category detail shop view
class ShopCategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            # Are we trying to fetch the detail for the Highlighted section?
            if category_slug == HighlightManager.slug:
                return HighlightManager.getHighlightCategoryDetail()
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        all_categories = Category.objects.all()

        if category:
            serializer = CategorySerializer(category)
            all_categories_serializer = CategoryShopListSerializer(all_categories, many=True)    
            categories_data = all_categories_serializer.data

            # Do we have any highlighted products to display?
            if HighlightManager.shouldDisplayHighlights():
                categories_data.append(HighlightManager.getHighlightCategory())

            if serializer.is_valid:
                return ResponseManager.build_successful_response({
                    'category_detail': serializer.data,
                    'all_categories': categories_data
                    })
            else: 
                return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "There has been an issue fetching the category you are trying to view. Please try again later.")
        
        return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, "Category not found. Please try again later.")

# Registration view
class RegisterView(generics.GenericAPIView):

    def post(self, request):
        user = request.data
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # Fetch the current User Model Object
        user = User.objects.get(email=user_data['email'])

        # Retrieve the access token for the user by the user ID
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request)
        relative_link = reverse('verify-email')
        absolute_url = f'http://{current_site}{relative_link}?token={str(token)}'

        email_body = f'Hello {user.name}. Thanks for signing up with us, please press the link below to verify your account. \n{absolute_url}'
        email_subject = f'{user.name}, verify your account for iPadel'
        email_data = {
            'to': user.email,
            'body': email_body,
            'subject': email_subject
        }

        # Send the registration email
        EmailManager.sendEmail(email_data)

        return ResponseManager.build_successful_response({
            'user_data': user_data
        })

# Email verification view
class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])

            if user:
                # Verify the user
                user.is_verified = True
                user.save()
                return ResponseManager.build_successful_response({
                    'result' : f'Good news {user.name}, your account has been successfuly verified!'
                    })

        except jwt.ExpiredSignatureError:
            # Delete the user to allow the customer to sign up again with the same details
            user.delete()
            return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 'The activation link has expired for security reasons. You can generate a new one by registering again.')
        except jwt.exceptions.DecodeError:
            return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 'There has been an error with your verification link. Please try again or contact a member of staff.')

# Login view
class LoginView(generics.GenericAPIView):
    serializer = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer(data=user)
        serializer.is_valid(raise_exception=True)

        return ResponseManager.build_successful_response({
            'result' : serializer.data
            })

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)

        if serializer.is_valid:
            return ResponseManager.build_successful_response({
                'result' : serializer.data
                })
    else:
        return ResponseManager.build_successful_response({})