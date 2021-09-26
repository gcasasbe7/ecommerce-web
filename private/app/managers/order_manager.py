import stripe
from ..models import Product, User
import jwt
from django.conf import settings

class OrderManager:

    '''
    Validates the order information
    Ensures the basket content is valid
    Ensures the user is eligible to place an order
    basket      = {'basket_creation_datetime': value, 'basket_content': []}
    user_data   = {'token': value, 'name' : value, 'last_name' : value, 'phone' : value, 
                   'address' : value, 'zipcode' : value, 'location' : value,}
    @returns order = {
        'valid':        value,
        'total_amount': value
        'errors:        [],  
    }
    '''
    @staticmethod
    def check_order(basket, user):
        # Initialize response structure
        order = {
            'valid': '',
            'total_amount': '',
            'errors': []
        }

        # Check if the user is eligible to place an order
        user_validation = OrderManager.check_user(user)
        # Check if the basket is valid
        basket_validation = OrderManager.check_basket(basket)
        # Global validation
        order['valid'] = user_validation['valid'] and basket_validation['valid']
        # Is the user and order data valid to proceed?
        if order['valid']:
            # Buffer the total price of the order
            order['total_amount'] = basket_validation['total_amount']
        else:
            # Buffer the relevant errors
            order['errors'] = user_validation['errors'] + basket_validation['errors']

        return order
        
    '''
    Validates the user given a token
    Ensures the user exists and is eligible to place orders
    @returns response = {
        'valid': '',
        'errors': []
    } 
    '''
    def check_user(user):
        # Define the response structure
        response = {
            'valid': '',
            'errors': []
        }

        try:
            # Does the user exist?
            if user:

                # Is the user verified?
                if not user.is_verified:
                    response['valid'] = False
                    response['errors'].append("Your account is not verified. Please verify your account before placing orders")

                # Is the user eligible to place orders?
                elif not user.is_active:
                    response['valid'] = False
                    response['errors'].append("You are currently unable to place orders. Contact a member of staff")

                # Valid user
                else:
                    response['valid'] = True

            # Invalid user
            else:
                response['valid'] = False
                response['errors'].append("We couldn't verify the user. Please try again later or contact a member of staff")

        except Exception:
            response['valid'] = False
            response['errors'].append("We couldn't validate the user. Please try again later or contact a member of staff")
    
        return response

    '''
    Validates the given basket of products
    Ensures all the products are availble, ready to be sold and in stock.
    @returns response = {
        'valid': '',
        'total_amount': '',
        'errors': []
    } 
    '''
    def check_basket(basket):
        # Define the response structure
        response = {
            'valid': True,
            'total_amount': 0,
            'errors': []
        }

        # Loop the basket content
        for item in basket['basket_content']:
            # Sanitze the basket item
            item_validation = OrderManager.is_product_available(item)
            # Is this item available?
            if item_validation['valid']:
                # Accumulate the price
                response['total_amount'] += OrderManager.get_item_total(item)
            else:
                # Invalid item
                response['valid'] = False
                response['errors'].append(item_validation['error'])

        return response

    '''
    Determines the availability of a product ensuring it is displayable and in stock
    '''
    def is_product_available(item):
        # Define the response structure
        response = {
            'valid': True,
            'error': ''
        }
        try:
            # Decapsulate the item
            product_id      = item['product_id']
            desired_amount  = item['quantity']
            # Get the product
            product = Product.objects.get(id=product_id)
            # Is the product available?
            if not product.show:
                response['valid'] = False
                response['error'] = f'The product "{product.name}" is currently unavailable'

            elif product.stock < desired_amount:
                response['valid'] = False
                word = 'item' if product.stock == 1 else 'items'
                response['error'] = f'Unfortunately we just have {product.stock} {word} left for the product "{product.name}". Adjust the amount or let us inform you instantly when the product is available again.'
        
        except Product.DoesNotExist:
            response['valid'] = False
            response['error'] = 'There has been an issue with one of the products of your basket. Please try again later or contact a member of staff if the problem persists'

        return response

    '''
    Calculates the total price of an item
    item = {'product_id': value, 'quantity': value}
    * Assumes the product_id of the item is valid
    '''
    def get_item_total(item):
        return round(Product.objects.get(id=item['product_id']).price * item['quantity'], 2)

    '''
    Converts euro value to the minimal cent value
    '''
    @staticmethod
    def eur_to_cent(value):
        return int(value * 100)