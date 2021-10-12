from django.urls import path
# Shop views
from .views.shop_views import *
# Identification views
from .views.identification_views import *
# Reset password views
from .views.reset_password_views import *
# Checkout views
from .views.checkout_views import *


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('verify-email/', VerifyEmail.as_view(), name="verify-email"),
    path('request-reset-password/', RequestResetPassword.as_view(), name="request-reset-password"),
    path('check-reset-password/<uidb64>/<token>/', ResetPasswordCheckTokenView.as_view(), name="check-reset-password"),
    path('complete-reset-password/', SetNewPasswordView.as_view(), name="complete-reset-password"),

    path('products/search/', search),
    path('categories/', CategoriesList.as_view()),
    path('shop/<slug:category_slug>/', ShopCategoryDetail.as_view()),
    path('shop/<slug:category_slug>/<slug:product_slug>/', ShopProductDetail.as_view()),

    path('checkout/', CreatePaymentIntentView.as_view()),
]