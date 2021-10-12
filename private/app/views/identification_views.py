import os
import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import RegisterSerializer, LoginSerializer
from ..models import User
from ..managers.email_manager import EmailManager
from ..managers.response_manager import ResponseManager


'''
Registration View
- Handles the user registration
Allowed HTTP methods: POST
Requires authentication: NO
'''
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

        # Build the email verification url
        base_frontend_url = os.environ.get('FRONTEND_BASE_URL')
        absolute_url = f'{base_frontend_url}/account/verify-email/?token={str(token)}'

        # Build the email structure
        email_body = f'Hello {user.name}. Thanks for signing up with us, please press the link below to verify your account. \n{absolute_url}'
        email_subject = f'{user.name}, verify your account for iPadel'
        email_data = {
            'to': user.email,
            'body': email_body,
            'subject': email_subject
        }

        # Send the registration email
        EmailManager.sendEmail(email_data)

        # Return the successful responsee to the forntend application
        return ResponseManager.build_successful_response({
            'user_data': user_data
        })

'''
Email Verification View
- Handles the user email verification after a successful registration
Allowed HTTP methods: GET
Requires authentication: NO
'''
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
            # TODO INSTEAD OF DELETING, SEND A NEW EMAIL WITH A NEW VALID ACCESS TOKEN FOR THE USER
            user.delete()
            return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 
                'The activation link has expired for security reasons. You can generate a new one by registering again.')

        except jwt.exceptions.DecodeError:
            return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 
                'There has been an error with your verification link. Please try again or contact a member of staff.')

'''
Login View
- Handles the user identification into the application
Allowed HTTP methods: POST
Requires authentication: NO
'''
class LoginView(APIView):

    serializer = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer(data=user)
        serializer.is_valid(raise_exception=True)

        return ResponseManager.build_successful_response({
            'result': serializer.data
        })