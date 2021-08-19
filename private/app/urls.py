from typing import AnyStr
from django.urls import path, include
from app import views

urlpatterns = [
    path('products', views.AllProductsView.as_view()),
    path('categories', views.CategoriesList.as_view()),
    path('shop', views.ShopView.as_view()),

    path('shop/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('shop/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
]