from rest_framework import serializers
from .models import *

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('image',)

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ('name',)

class ProductSerializer(serializers.ModelSerializer):
    type = ProductTypeSerializer()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'type',
            'description',
            'price',
            'get_absolute_url',
            'get_thumbnail',
            'images'
        )