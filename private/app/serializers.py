from rest_framework import serializers
from .models import *

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
        fields = ('id','name','absolute_url', 'image_url')

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
            'id',
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
