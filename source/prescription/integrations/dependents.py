from django.conf import settings

import requests
from requests.adapters import HTTPAdapter
from requests.models import HTTPError
from requests.sessions import session

from prescription.utils import CustomExceptionError


def set_session(name_endpoint):
    session = requests.Session()
    http_adapter = requests.adapters.HTTPAdapter(max_retries=dict(settings.TRIES).get(name_endpoint))
    session.mount('https://', http_adapter)
    return session

def set_headers(name_endpoit):
    token = dict(settings.TOKENS_BEARER).get(name_endpoit)

    headers = {
        'Authorization': f'Bearer {token}'
    }

    return headers

def request_clinics(id):
    headers = set_headers('CLINICS')
    try:
        http = set_session('CLINICS')
        host = dict(settings.HOST_DEPENDENTS).get('CLINICS').rstrip('/')
        response = http.get(f'{host}/clinics/{id}',headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError:
        return None

def request_physician(id):
    headers = set_headers('PHYSICIANS')
    try:
        http = set_session('PHYSICIANS')
        host  = dict(settings.HOST_DEPENDENTS).get('PHYSICIANS').rstrip('/')
        response = http.get(f'{host}/physicians/{id}', headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as err:
        if err.response.status_code == 404:
            raise CustomExceptionError("02")
        elif err.response.status_code == 400:
            raise CustomExceptionError("05")

def request_patient(id):

    headers = set_headers('PATIENTS')
    try:
        http = set_session('PATIENTS')
        host = dict(settings.HOST_DEPENDENTS).get('PATIENTS').rstrip('/')
        response = http.get(f'{host}/patients/{id}', headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as err:
        if err.response.status_code == 404:
            raise CustomExceptionError("03")
        elif err.response.status_code == 400:
            raise CustomExceptionError("06")


def integrate_metrics(instance):
    pass