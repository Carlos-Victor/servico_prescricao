from django.shortcuts import render
from django.db import transaction
import requests

from rest_framework import viewsets, status
from rest_framework.response import Response

from prescription.models import Prescription
from prescription.serializers import PrescriptionsSerializer
from prescription.utils import CustomExceptionError

# Create your views here.



class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionsSerializer


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = Prescription.objects.create(
                clinic=request.data['clinic'].get('id'),
                physician=request.data['physician'].get('id'),
                patient=request.data['patient'].get('id'),
                text=request.data['text']
            )
            # integrate_metrics(instance)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            # REALIZAR CONSULTA DE APLICAÇÕES EXTERNAS
        raise CustomExceptionError("01")
