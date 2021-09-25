from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, name, email, surname, password=None):
        if name is None or surname is None or email is None or password is None:
            raise TypeError("Invalid values")

        user = self.model(name=name, surname=surname, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, name, email, surname, password=None):
        user = self.create_user(name, email, surname, password)
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    added_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} {self.surname}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {'access_token' : str(refresh_token.access_token), 'refresh_token' : str(refresh_token)}

    @property
    def is_staff(self):
        return self.is_admin

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='uploads/brand_logos/')

    def __str__(self):
        return self.name

    def logo_url(self):
        return f'http://127.0.0.1:8000/media/{self.logo}/'

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
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
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    stock = models.IntegerField()
    highlight = models.BooleanField(default=False)
    show = models.BooleanField(default=True)

    class Meta:
        ordering = ('-added_date',)

    def __str__(self):
        return self.name + ( ' (*)' if self.highlight else '')

    def is_available(self):
        return self.stock > 0

    def absolute_url(self):
        return f'/shop/{self.category.slug}/{self.slug}/'

    @property
    def image_absolute_url(self):
        return f'http://127.0.0.1:8000/media/{self.cover_image}/'

    @property
    def truncated_description(self):
        return self.description[0:48] + '...'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    images = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)

    def __str__(self):
        return self.product.name + " image (" + str(self.images) + ")"
    
    def absolute_url(self):
        return f'http://127.0.0.1:8000/media/{self.images}/'

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=False, blank=False)
    stripe_checkout_session_id = models.CharField(max_length=255, null=False, blank=False)
    stripe_payment_intent_id = models.CharField(max_length=255, null=False, blank=False)
    basket = models.JSONField()
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'[{self.status}] Order by {self.user.name} ({self.total_amount}€ in {self.basket_size} products)'

    @property
    def status(self):
        headers = {'Authorization': f'Bearer {settings.STRIPE_API_KEY}'}
        req = requests.get(
            url=f'https://api.stripe.com/v1/checkout/sessions/{self.stripe_checkout_session_id}',
            headers=headers
        )
        if req.status_code == 200:
            return req.json()['payment_status'].capitalize()
        return '-'

    @property
    def total_amount(self):
        total=0
        try:
            for item in self.basket['basket_content']:
                total += round(Product.objects.get(id=item['product_id']).price * item['quantity'], 2)
        except Exception:
            return -1
        return total

    @property
    def basket_size(self):
        acc=0
        for item in self.basket['basket_content']:
            acc += item['quantity']
        return acc