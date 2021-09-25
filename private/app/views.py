from django.http.response import HttpResponse
import jwt
import os
import stripe
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.urls import reverse
from django.utils.encoding import (smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .managers.email_manager import EmailManager
from .managers.highlight_manager import HighlightManager
from .managers.response_manager import ResponseManager
from .managers.thread_manager import CheckOrderThread
from .managers.order_manager import OrderManager
from .models import *
from .serializers import *

# Set the stripe API Key
stripe.api_key = settings.STRIPE_API_KEY

# Product detail shop view
class ShopProductDetail(APIView):
    def get_object(self, product_slug, category_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            return None

    def get(self, request, product_slug, category_slug, format=None):
        product = self.get_object(product_slug, category_slug)

        if product:
            serializer = ProductSerializer(product)

            if serializer.is_valid:
                return ResponseManager.build_successful_response({
                    'product': serializer.data
                })
            else:
                return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "There has been an issue with the product you are trying to view. Please try again later.")

        return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, "Product not found. Please try again later.")

# Categories list including Hihglighted section if valid
class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategoryShopListSerializer(categories, many=True)

        if serializer.is_valid:
            return ResponseManager.build_successful_response({
                'categories': serializer.data,
                'highlight': HighlightManager.getHighlightCategory() if HighlightManager.shouldDisplayHighlights() else ''
            })
        else:
            return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "There has been an issue with some category you are trying to view. Please try again later.")

# Category detail shop view
class ShopCategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            # Are we trying to fetch the detail for the Highlighted section?
            if category_slug == HighlightManager.slug:
                return HighlightManager.getHighlightCategoryDetail()
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        all_categories = Category.objects.all()

        if category:
            serializer = CategorySerializer(category)
            all_categories_serializer = CategoryShopListSerializer(
                all_categories, many=True)
            categories_data = all_categories_serializer.data

            # Do we have any highlighted products to display?
            if HighlightManager.shouldDisplayHighlights():
                categories_data.append(HighlightManager.getHighlightCategory())

            if serializer.is_valid:
                return ResponseManager.build_successful_response({
                    'category_detail': serializer.data,
                    'all_categories': categories_data
                })
            else:
                return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "There has been an issue fetching the category you are trying to view. Please try again later.")

        return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, "Category not found. Please try again later.")

# Registration view
class RegisterView(APIView):

    def post(self, request):
        user = request.data
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        # Fetch the current User Model Object
        user = User.objects.get(email=user_data['email'])

        # Retrieve the access token for the user by the user ID
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('verify-email')
        absolute_url = f'http://{current_site}{relative_link}?token={str(token)}'

        email_body = f'Hello {user.name}. Thanks for signing up with us, please press the link below to verify your account. \n{absolute_url}'
        email_subject = f'{user.name}, verify your account for iPadel'
        email_data = {
            'to': user.email,
            'body': email_body,
            'subject': email_subject
        }

        # Send the registration email
        EmailManager.sendEmail(email_data)

        return ResponseManager.build_successful_response({
            'user_data': user_data
        })

# Email verification view
class VerifyEmail(APIView): 
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])

            if user:
                # Verify the user
                user.is_verified = True
                user.save()
                return ResponseManager.build_successful_response({
                    'result': f'Good news {user.name}, your account has been successfuly verified!'
                })

        except jwt.ExpiredSignatureError:
            # Delete the user to allow the customer to sign up again with the same details
            user.delete()
            return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 'The activation link has expired for security reasons. You can generate a new one by registering again.')
        except jwt.exceptions.DecodeError:
            return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 'There has been an error with your verification link. Please try again or contact a member of staff.')

# Login view
class LoginView(APIView):
    serializer = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer(data=user)
        serializer.is_valid(raise_exception=True)

        return ResponseManager.build_successful_response({
            'result': serializer.data
        })

# Search in all products Api View
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)

        if serializer.is_valid:
            return ResponseManager.build_successful_response({
                'result': serializer.data
            })
    else:
        return ResponseManager.build_successful_response({})

# Request a new reset password token
class RequestResetPassword(APIView):
    serializer = ResetPasswordSerializer

    def post(self, request):
        email = request.data['email']

        # Can we get the user through email?
        if User.objects.filter(email=email).exists():
            # Fetch the user
            user = User.objects.get(email=email)
            # Encode the user id
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            # Generate the reset password token for the current user
            token = PasswordResetTokenGenerator().make_token(user)
            # Build the reset password link
            base_frontend_url = os.environ.get('FRONTEND_BASE_URL')
            absolute_url = f'{base_frontend_url}/account/reset-password/{uidb64}/{token}'
            # Build the email
            email_body = f'Hello {user.name}. To reset your password press the link below. \n{absolute_url}'
            email_subject = f'{user.name}, reset your password for iPadel'
            email_data = {
                'to': user.email,
                'body': email_body,
                'subject': email_subject
            }
            # Send the reset password email
            EmailManager.sendEmail(email_data)
            # Build the success response
            return ResponseManager.build_successful_response({
                'result': 'An email to reset your password has been sent to your email'
            })
        else:
            # Build the invalid response with the error
            return ResponseManager.build_invalid_response(status.HTTP_406_NOT_ACCEPTABLE, "We couldn't find your email, please make sure you are introducing the correct address")

# Check the validity of the password reset attempt
class ResetPasswordCheckTokenView(APIView):

    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 'The reset password link has expired for security reasons. Please repeat the resetting password process to generate a new valid link')

            # Return success response
            return ResponseManager.build_successful_response({
                'uidb64': uidb64,
                'token': token
            })
        except User.DoesNotExist:
            return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, 'The reset password link is not valid for your user. Please try again or contact a member of staff')

# Set new password View
class SetNewPasswordView(APIView):
    serializer = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return ResponseManager.build_successful_response({
            'result': 'Your password has been reset successfuly.'
        })

# Creates a Stripe Payment Intent if the basket content and the user are valid
class CreatePaymentIntentView(APIView):

    permission_classes = (IsAuthenticated,)
    
    def post(self, request):

        data = request.data
        
        try:
            # Fetch the values from the request
            basket      = data['basket']
            user_data   = data['user_data']

            # Valid request data?
            if not basket or not user_data:
                return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 
                'Invalid request')
        
            # Declare the check order thread
            order_thread = CheckOrderThread(basket=basket, user_data=user_data)
            # Perform a sanity check to the order in a background thread
            order_thread.start()
            # Obtain the data from the thread safely
            order = order_thread.join()
            
            # Prepare the response
            if order['valid']:
                # Create the stripe Payment Intent
                intent = stripe.PaymentIntent.create(
                    amount=OrderManager.eur_to_cent(order['total_amount']),
                    currency=settings.APP_CURRENCY
                )
                # Return the client secret
                return ResponseManager.build_successful_response({
                    'client_secret': intent['client_secret']
                })

                # Create a new Order
                # order = {
                #     "user": order['user'],
                #     "stripe_checkout_session_id": session.id,
                #     "stripe_payment_intent_id": session.payment_intent,
                #     "basket": basket,
                # }
                #    
                # serializer = OrderSerializer(data=order)
                # 
                # if serializer.is_valid():
                #     # Save the order
                #     order_instance = serializer.save()

            else:
                return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 
                ', '.join(order['errors']))

        except Exception as ex:
            return ResponseManager.build_invalid_response(status.HTTP_500_INTERNAL_SERVER_ERROR, 
                f"There has been an issue with the server. Please try again later ({str(ex)})")

'''
WebHook to retain real time information frmo the Checkout procedures
Events handled in this webhook:
- Checkout session payment failed:       checkout.session.async_payment_failed
- Checkout session payment succeeded:    checkout.session.async_payment_succeeded
- Checkout session completed:            checkout.session.completed
- Checkout session expired:              checkout.session.expired
'''
@csrf_exempt
@require_POST
def checkout_stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = settings.STRIPE_CHECKOUT_SESSION_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Events handling
    if event['type'] == 'payment_intent.created':
        payment_intent = event['data']['object']
        print(f"\n\n\n\n\n\nPAYMENT INTENT CREATED!\n\n\n\n\n\n")
    if event['type'] == 'checkout.session.async_payment_failed':
        checkout = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        checkout = event['data']['object']
        print(f"\n\n\n\n\n\nPAYMENT SUCCEEDED!\n\n\n\n\n\n")
    elif event['type'] == 'checkout.session.completed':
        checkout = event['data']['object']
        print(f"\n\n\n\n\n\nCHECKOUT SESSION COMPLETED!\n\n\n\n\n\n")
    elif event['type'] == 'checkout.session.expired':
        checkout = event['data']['object']

    else:
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)



class TestView(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        
        # ok = stripe.Price.list()
        # product = Product.objects.get(id=4)
        # stripe_product = stripe.Product.create(
        #     api_key=settings.STRIPE_API_KEY,
        #     id=product.id,
        #     name=product.name,
        #     description=product.description,
        #     images=[product.image_absolute_url]
        # )

        # stripe_product_price = stripe.Price.create(
        #     api_key=settings.STRIPE_API_KEY,
        #     unit_amount=OrderManager.eur_to_cent(product.price),
        #     currency=settings.APP_CURRENCY,
        #     product=stripe_product.id
        # )

        # # stripe_product = stripe.Product.retrieve('1')

        return ResponseManager.build_successful_response({
            'result': request.META['STRIPE_SECRET_KEY'],
        })