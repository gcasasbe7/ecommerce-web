from io import BytesIO
from PIL import Image
from django.db import models
from django.core.files import File

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='uploads/brand_logos/')

    def __str__(self):
        return self.name

    def logo_url(self):
        return f'http://127.0.0.1:8000/media/{self.logo}/'

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='uploads/category_images/', blank=True, null=True)
    visible = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    # Returns the absolute url for this product type using the slug attribute
    def absolute_url(self):
        return f'/shop/{self.slug}'

    def image_url(self):
        return f'http://127.0.0.1:8000/media/{self.image}/'

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='products')
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateField(auto_now_add=True)
    display_image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    stock = models.IntegerField()

    class Meta:
        ordering = ('-added_date',)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.stock > 0

    # Returns the absolute url for this product using the slug attribute
    def absolute_url(self):
        return f'/shop/{self.main_category.slug}/{self.slug}/'

    def image_absolute_url(self):
        return f'http://127.0.0.1:8000/media/{self.display_image}/'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)

    def __str__(self):
        return self.product.name + " image (" + str(self.id) + ")"
    
    def absolute_url(self):
        return f'http://127.0.0.1:8000/media/{self.image}/'