from httmock import urlmatch, response



class MockClinics:

    @urlmatch(path='/v1/clinics/200')
    def mock_clinic_200(url, request):
        return response(200, {"id": "1","name": "Joe Doe"})

    @urlmatch(path='/v1/clinics/503')
    def  mock_clinic_503(url, request):
        return response(503, {})

    @urlmatch(path='/v1/clinics/504')
    def mock_clinic_504(url, request):
        return response(504, {})

    @urlmatch(path='/v1/clinics/404')
    def mock_clinic_404(url, request):
        return response(404, {})

class MockPhysicians:

    @urlmatch(path='/v1/physicians/200')
    def mock_physician_200(url, request):
        return response(200, { "id": "1", "name": "Joe Doe", "crm": "CRM" })

    @urlmatch(path='/v1/physicians/503')
    def  mock_physician_503(url, request):
        return response(503, {})

    @urlmatch(path='/v1/physicians/504')
    def mock_physician_504(url, request):
        return response(504, {})

    @urlmatch(path='/v1/physicians/404')
    def mock_physician_404(url, request):
        return response(404, {})

class MockPatients:

    @urlmatch(path='/v1/patients/200')
    def mock_patient_200(url, request):
        return response(200, {"id": "1","name": "Joe Doe","email": "test@gmail.com","phone": "2-222-222-2222"},)

    @urlmatch(path='/v1/patients/503')
    def  mock_patient_503(url, request):
        return response(503, {})

    @urlmatch(path='/v1/patients/504')
    def mock_patient_504(url, request):
        return response(504, {})

    @urlmatch(path='/v1/patients/404')
    def mock_patient_404(url, request):
        return response(404, {})


class MockMetrics:

    @urlmatch(path='/v1/metrics')
    def mock_metrics_201(url, request):
        return response(201, { "id": "1", "clinic_id": 1, "clinic_name": "Clinica A", "physician_id": 1, "physician_name": "Dr. João", "physician_crm": "SP293893",
                            "patient_id": 1, "patient_name": "Rodrigo", "patient_email": "rodrigo@gmail.com", "patient_phone": "(16)998765625"})

    @urlmatch(path='/v1/metrics')
    def  mock_metrics_503(url, request):
        return response(503, {})

    @urlmatch(path='/v1/metrics')
    def  mock_metrics_504(url, request):
        return response(504, {})