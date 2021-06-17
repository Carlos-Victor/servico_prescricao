from django.conf import settings

from rest_framework.exceptions import ValidationError, APIException
from rest_framework import status


    

class CustomExceptionError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def return_error_message(self, code):
        message_list = dict(settings.ERROR_REST).get(code)
        if message_list:
            return message_list

    def __init__(self, code):
        if code:
            self.detail = {
                "error": {
                    "message": self.return_error_message(code),
                    "code": code
                }
            }

# def parse_metrics():

# '{
#   "clinic_id": 1,
#   "clinic_name": "Clínica A",
#   "physician_id": 1,
#   "physician_name": "José",
#   "physician_crm": "SP293893",
#   "patient_id": 1,
#   "patient_name": "Rodrigo",
#   "patient_email": "rodrigo@gmail.com",
#   "patient_phone": "(16)998765625"
# }'