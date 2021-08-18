from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files import File

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='uploads/brand_logos/')

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    # Returns the absolute url for this product type using the slug attribute
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ProductType, related_name='product_type', on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    thumbnail = models.ImageField(upload_to='uploads/product_thumbnails/', blank=True, null=True)
    added_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-added_date',)

    def __str__(self):
        return self.name

    # Returns the absolute url for this product using the slug attribute
    def get_absolute_url(self):
        return f'/{self.slug}/'

    def get_thumbnail(self):
        if self.thumbnail:
            return "http://127.0.0.1:8000" + self.thumbnail.url

class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)

    def __str__(self):
        return self.product.name + " image"
    