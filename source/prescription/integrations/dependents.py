from django.conf import settings

import requests
from requests.exceptions import ConnectTimeout, RetryError
from requests.packages.urllib3.util.retry import Retry
from requests.models import HTTPError

from prescription.utils import CustomExceptionError


def set_session(name_endpoint):
    session = requests.Session()
    retry = Retry(
        total=dict(settings.TRIES).get(name_endpoint),
        read=dict(settings.TRIES).get(name_endpoint),
        connect=dict(settings.TRIES).get(name_endpoint),
        status_forcelist=(500, 502, 503),
    )
    http_adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', http_adapter)
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
        response = http.get(f'{host}/clinics/{id}',headers=headers, timeout=dict(settings.TIMEOUT_DEPENDENTS).get('CLINICS'))
        response.raise_for_status()
        data = response.json()
        data = {
            "clinic_id": data.get('id'),
            "clinic_name": data.get('name')
        }
        return data
    except (HTTPError, ConnectTimeout, RetryError):
        return None

def request_physician(id):
    headers = set_headers('PHYSICIANS')
    try:
        http = set_session('PHYSICIANS')
        host  = dict(settings.HOST_DEPENDENTS).get('PHYSICIANS').rstrip('/')
        response = http.get(f'{host}/physicians/{id}', headers=headers, timeout=dict(settings.TIMEOUT_DEPENDENTS).get('PHYSICIANS'))
        response.raise_for_status()
        data = response.json()
        data = {
            "physician_id": data.get('id'),
            "physician_name": data.get('name'),
            "physician_crm":  data.get('crm')
        }
        return data
    except (HTTPError, RetryError, ConnectTimeout) as err:
        if err.response.status_code == 404:
            raise CustomExceptionError("02")
        raise CustomExceptionError("05")

def request_patient(id):
    headers = set_headers('PATIENTS')
    try:
        http = set_session('PATIENTS')
        host = dict(settings.HOST_DEPENDENTS).get('PATIENTS').rstrip('/')
        response = http.get(f'{host}/patients/{id}', headers=headers, timeout=dict(settings.TIMEOUT_DEPENDENTS).get('PATIENTS'))
        response.raise_for_status()
        data = response.json()
        data = {
            "patient_id": data.get('id'),
            "patient_name": data.get('name'),
            "patient_email": data.get('email'),
            "patient_phone": data.get('phone')
        }
        return data
    except (HTTPError, RetryError, ConnectTimeout)as err:
        if err.response.status_code == 404:
            raise CustomExceptionError("03")
        raise CustomExceptionError("06")

def request_metrics(data):
    headers = set_headers('METRICS')
    try:
        http = set_session('METRICS')
        host = dict(settings.HOST_DEPENDENTS).get('METRICS').rstrip('/')
        response = http.post(f'{host}/metrics', data=data, headers=headers, timeout=dict(settings.TIMEOUT_DEPENDENTS).get('METRICS'))
        response.raise_for_status()
        return response.json()
    except (HTTPError, RetryError, ConnectTimeout):
        raise CustomExceptionError("04")

def parse_metrics(list_dependents):
    data = {
        "physician_id": 0,
        "physician_name": "",
        "physician_crm": "",
        "patient_id": 0,
        "patient_name": "",
        "patient_email": "",
        "patient_phone": ""
    }

    for data_dependent in list_dependents:
        data.update(data_dependent)

    return data

def integrate_metrics(instance):
    list_dependents = []

    data_clinics = request_clinics(instance.clinic)
    if data_clinics:
        list_dependents.append(data_clinics)

    data_physician = request_physician(instance.physician)
    if data_physician:
        list_dependents.append(data_physician)

    data_patient = request_patient(instance.patient)
    if data_patient:
        list_dependents.append(data_patient)

    data_metrics = parse_metrics(list_dependents)
    
    return data_metrics

def send_metrics(instance):
    data_metrics = integrate_metrics(instance)
    data = request_metrics(data_metrics)
    return data

