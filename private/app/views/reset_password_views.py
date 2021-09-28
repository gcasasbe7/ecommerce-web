import os
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ..serializers import ResetPasswordSerializer, SetNewPasswordSerializer
from ..models import User
from ..managers.email_manager import EmailManager
from ..managers.response_manager import ResponseManager

'''
Request Reset Password Link View
- Handles the request of a user to reset the account password
Allowed HTTP methods: POST
Requires authentication: NO
'''
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

'''
Check Reset Password Link View
- Handles the request of a user to reset the account password
Allowed HTTP methods: GET
Requires authentication: NO
'''
class ResetPasswordCheckTokenView(APIView):

    def get(self, request, uidb64, token):

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 
                    'The reset password link has expired for security reasons. Please repeat the resetting password process to generate a new valid link')

            # Return success response
            return ResponseManager.build_successful_response({
                'uidb64': uidb64,
                'token': token
            })

        except User.DoesNotExist:
            return ResponseManager.build_invalid_response(status.HTTP_404_NOT_FOUND, 'The reset password link is not valid for your user. Please try again or contact a member of staff')

'''
Set New Password View
- Handles the password resetting after a succesful password change request
Allowed HTTP methods: PATCH
Requires authentication: NO
'''
class SetNewPasswordView(APIView):
    
    serializer = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return ResponseManager.build_successful_response({
            'result': 'Your password has been reset successfuly.'
        })