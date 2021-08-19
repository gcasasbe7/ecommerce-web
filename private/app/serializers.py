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

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

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
            'images'
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