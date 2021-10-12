from rest_framework.response import Response
from rest_framework import status

# Class to manage all the API Responses to the front end application
## Response Structure (Rest Framework Response):
## - Status     (Response code)
## - Data       (Response data in JSON format)
## - Message    (Response message)
class ResponseManager:
    
    @staticmethod
    def build_successful_response(data):
        return ResponseManager.build_response(status.HTTP_200_OK, "OK", data)

    @staticmethod
    def build_invalid_response(response_code, message):
        return ResponseManager.build_response(response_code, message, {})

    # Root method to build the Response object
    def build_response(response_code, message, data):
        return Response({
            'status': response_code,
            'data': data,
            'message': message
        })