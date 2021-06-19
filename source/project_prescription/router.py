from rest_framework import routers

from prescription.views import PrescriptionViewSet



router = routers.DefaultRouter()

router.register('prescriptions', PrescriptionViewSet)
