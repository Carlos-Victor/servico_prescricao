from httmock import urlmatch, response



class MockClinics:

    @urlmatch(path='/clinics/1')
    def mock_clinic_200(url, request):
        pass

    @urlmatch(path='/clinics/2')
    def  mock_clinic_503(url, request):
        pass

    @urlmatch(path='/clinics/3')
    def mock_clinic_504(url, request):
        pass

    @urlmatch(path='/clinics/4')
    def mock_clinic_404(url, request):
        pass

class MockPhysicians:

    @urlmatch(path='/physician/1')
    def mock_physician_200(url, request):
        pass

    @urlmatch(path='/physician/2')
    def  mock_physician_503(url, request):
        pass

    @urlmatch(path='/physician/3')
    def mock_physician_504(url, request):
        pass

    @urlmatch(path='/physician/4')
    def mock_physician_404(url, request):
        pass

class MockPatients:

    @urlmatch(path='/patient/1')
    def mock_patient_200(url, request):
        pass

    @urlmatch(path='/patient/2')
    def  mock_patient_503(url, request):
        pass

    @urlmatch(path='/patient/3')
    def mock_patient_504(url, request):
        pass

    @urlmatch(path='/patient/4')
    def mock_patient_404(url, request):
        pass


class MockMetrics:

    @urlmatch(path='/metrics/1')
    def mock_metrics_201(url, request):
        pass

    @urlmatch(path='/metrics/2')
    def  mock_metrics_503(url, request):
        pass