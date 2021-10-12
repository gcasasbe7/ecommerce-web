import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..managers.thread_manager import CheckOrderThread
from ..managers.order_manager import OrderManager
from ..managers.response_manager import ResponseManager

# Set the stripe API Key
stripe.api_key = settings.STRIPE_API_KEY

# Creates a Stripe Payment Intent if the basket content and the user are valid
@authentication_classes([JWTAuthentication])
class CreatePaymentIntentView(APIView):

    def post(self, request):
        # Fetch the request data
        data = request.data
        
        try:
            # Fetch the values from the request
            basket = data['basket']

            # Valid request data?
            if not basket:
                return ResponseManager.build_invalid_response(status.HTTP_400_BAD_REQUEST, 'Invalid request')
        
            # Declare the check order thread
            order_thread = CheckOrderThread(basket=basket, user=request.user)
            # Perform a sanity check to the order in a background thread
            order_thread.start()
            # Safely wait and obtain the data from the thread when it's done
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