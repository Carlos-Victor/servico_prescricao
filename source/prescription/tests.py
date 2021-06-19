import json
from django.conf import settings

from httmock import HTTMock

from rest_framework.test import APITestCase

from prescription.mock_tests import MockClinics, MockPhysicians, MockPatients, MockMetrics
from prescription.models import Prescription
from prescription.integrations.dependents import integrate_metrics, request_clinics
from prescription.utils import CustomExceptionError

# Create your tests here.


class PrescriptionTest(APITestCase):

    def setUp(self):
        return super().setUp()


    def test_return_error_clinic_process_not_error(self):
        with HTTMock(MockClinics.mock_clinic_503, MockPhysicians.mock_physician_200, MockPatients.mock_patient_200, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 503},"physician": {"id": 200},"patient": {"id": 200},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(201, request.status_code)
            self.assertJSONEqual(json.dumps({"id": request.json()['id'],"clinic":{"id":503},"physician":{"id":200},"patient":{"id":200},"text":"Dipirona 1x ao dia"}), request.json())


    def test_return_data_metrics_not_clinics(self):
        with HTTMock(MockClinics.mock_clinic_503, MockPhysicians.mock_physician_200, MockPatients.mock_patient_200, MockMetrics.mock_metrics_201):
            instance = Prescription.objects.create(clinic=503, physician=200, patient=200, text="Teste")
            data_send_metrics = integrate_metrics(instance)
            self.assertNotIn('clinic_id', data_send_metrics)
            self.assertNotIn('clinic_name', data_send_metrics)


    def test_return_none_clinics_error(self):
        with HTTMock(MockClinics.mock_clinic_503, MockClinics.mock_clinic_404):
            data_send_clinics = request_clinics(503)
            self.assertIsNone(data_send_clinics)
            data_send_clinics = request_clinics(404)
            self.assertIsNone(data_send_clinics)
            data_send_clinics = request_clinics(504)
            self.assertIsNone(data_send_clinics)


    def test_malformed_request(self):
        with HTTMock(MockClinics.mock_clinic_503, MockPhysicians.mock_physician_200, MockPatients.mock_patient_200, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": 503,"physician": 200,"patient": 200 ,"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("01")).replace("'","\""))), request.json())


    def test_response_physician_not_found(self):
        with HTTMock(MockClinics.mock_clinic_200, MockPhysicians.mock_physician_404, MockPatients.mock_patient_200, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 200},"physician": {"id": 404},"patient": {"id": 200},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("02")).replace("'","\""))), request.json())



    def test_response_physician_no_available(self):
        with HTTMock(MockClinics.mock_clinic_503, MockPhysicians.mock_physician_503, MockPatients.mock_patient_200, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 503},"physician": {"id": 503},"patient": {"id": 200},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("05")).replace("'","\""))), request.json())


    def test_response_patient_not_found(self):
        with HTTMock(MockClinics.mock_clinic_503, MockPhysicians.mock_physician_200, MockPatients.mock_patient_404, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 503},"physician": {"id": 200},"patient": {"id": 404},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("03")).replace("'","\""))), request.json())


    def test_response_patient_no_available(self):
        with HTTMock(MockClinics.mock_clinic_503, MockPhysicians.mock_physician_200, MockPatients.mock_patient_503, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 503},"physician": {"id": 200},"patient": {"id": 503},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("06")).replace("'","\""))), request.json())


    def test_response_metrics_no_available(self):
        with HTTMock(MockClinics.mock_clinic_200, MockPhysicians.mock_physician_200, MockPatients.mock_patient_200, MockMetrics.mock_metrics_503):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 200},"physician": {"id": 200},"patient": {"id": 200},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("04")).replace("'","\""))), request.json())


    def test_response_clinics_timeout(self):
        settings.TRIES = (
            ('CLINICS', 0.001),
            ('PHYSICIANS', 0.001),
            ('PATIENTS', 0.001),
            ('METRICS', 0.001),
        )
        with HTTMock(MockClinics.mock_clinic_504, MockPhysicians.mock_physician_200, MockPatients.mock_patient_200, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 504},"physician": {"id": 200},"patient": {"id": 200},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(201, request.status_code)
            self.assertJSONEqual(json.dumps({"id": request.json()['id'],"clinic":{"id":504},"physician":{"id":200},"patient":{"id":200},"text":"Dipirona 1x ao dia"}), request.json())


    def test_response_physician_timeout(self):
        with HTTMock(MockClinics.mock_clinic_200, MockPhysicians.mock_physician_504, MockPatients.mock_patient_200, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 200},"physician": {"id": 504},"patient": {"id": 200},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("05")).replace("'","\""))), request.json())


    def test_response_patients_timeout(self):
        with HTTMock(MockClinics.mock_clinic_200, MockPhysicians.mock_physician_200, MockPatients.mock_patient_504, MockMetrics.mock_metrics_201):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 200},"physician": {"id": 200},"patient": {"id": 504},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("06")).replace("'","\""))), request.json())


    def test_response_metrics_timeout(self):
        with HTTMock(MockClinics.mock_clinic_200, MockPhysicians.mock_physician_200, MockPatients.mock_patient_200, MockMetrics.mock_metrics_504):
            request = self.client.post('http://testserver/prescriptions/', data={"clinic": {"id": 200},"physician": {"id": 200},"patient": {"id": 200},"text": "Dipirona 1x ao dia"}, format='json')
            self.assertEqual(400, request.status_code)
            self.assertJSONEqual(json.dumps(json.loads(str(CustomExceptionError("04")).replace("'","\""))), request.json())