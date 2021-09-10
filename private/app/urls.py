from typing import AnyStr
from django.urls import path
from app import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('verify-email/', views.VerifyEmail.as_view(), name="verify-email"),
    path('request-reset-password/', views.RequestResetPassword.as_view(), name="request-reset-password"),
    path('check-reset-password/<uidb64>/<token>/', views.ResetPasswordCheckTokenView.as_view(), name="check-reset-password"),
    path('complete-reset-password/', views.SetNewPasswordView.as_view(), name="complete-reset-password"),

    path('products/search/', views.search),
    path('categories/', views.CategoriesList.as_view()),
    path('shop/<slug:category_slug>/', views.ShopCategoryDetail.as_view()),
    path('shop/<slug:category_slug>/<slug:product_slug>/', views.ShopProductDetail.as_view()),
]