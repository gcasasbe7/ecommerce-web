from typing import AnyStr
from django.urls import path
from app import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('verify-email/', views.VerifyEmail.as_view(), name="verify-email"),

    path('products', views.AllProductsView.as_view()),
    path('products/search/', views.search),
    path('categories', views.CategoriesList.as_view()),

    path('shop/<slug:category_slug>/', views.ShopCategoryDetail.as_view()),
    path('shop/<slug:category_slug>/<slug:product_slug>/', views.ShopProductDetail.as_view()),
]