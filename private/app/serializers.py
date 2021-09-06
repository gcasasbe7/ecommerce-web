from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('absolute_url',)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('name', 'logo_url')

class CategoryShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','absolute_url', 'image_url')

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'brand',
            'description',
            'price',
            'absolute_url',
            'image_absolute_url',
            'images',
            'is_available'
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'name',
            'absolute_url',
            'image_url',
            'products',
        )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')        

    def validate(self, attrs):
        email = attrs.get('email', '')
        name = attrs.get('name', '')
        surname = attrs.get('surname', '')

        # Valid email?
        if not email:
            raise serializers.ValidationError("Please introduce a valid email")

        # Valid name?
        if not name or not name.isalnum():
            raise serializers.ValidationError("Please introduce a valid name")

        # Valid surname?
        if not surname:
            raise serializers.ValidationError("Please introduce a valid surname")

        return attrs

    def create(self, validated_data):
        # Override with our own definition of User
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(read_only=True)
    surname = serializers.CharField(read_only=True)
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'surname', 'tokens')

    def validate(self, attrs):
        # Fetch the user login data
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        # Attempt to authenticate
        user = auth.authenticate(email=email, password=password)
        # Raise exception for unvalid authentication
        if not user:
            raise AuthenticationFailed('Invalid credentials, please try again.')
        # Assert the account is verified
        if not user.is_verified:
            raise AuthenticationFailed('Account not verified, please verify your account before loging in.')
        # Assert the account is not blocked
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, please contact support.')
        
        return {
            'email': user.email,
            'name': user.name,
            'surname': user.surname,
            'tokens': user.tokens
        }