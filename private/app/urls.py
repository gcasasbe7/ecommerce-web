from typing import AnyStr
from django.urls import path, include
from app import views

urlpatterns = [
    path('all-products', views.AllProductsView.as_view()),
]