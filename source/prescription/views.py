from django.shortcuts import render
from django.db import transaction
import requests
import json

from rest_framework import viewsets, status
from rest_framework.response import Response

from prescription.serializers import PrescriptionsSerializer
from prescription.utils import CustomExceptionError
from prescription.integrations.dependents import send_metrics
from prescription.models import Prescription
# Create your views here.



class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionsSerializer
    http_method_names = ['post', 'head', 'options']

    # @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = json.loads(json.dumps(serializer.data))
            instance = Prescription.objects.create(
                clinic=data.get('clinic').get('id').get('id'),
                physician=data.get('physician').get('id').get('id'),
                patient=data.get('patient').get('id').get('id'),
                text=data.get('text')
            )
            send_metrics(instance)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status.HTTP_201_CREATED)
        raise CustomExceptionError("01")