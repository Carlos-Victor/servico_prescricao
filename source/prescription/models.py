from django.db import models

# Create your models here.

class Prescription(models.Model):
    clinic = models.IntegerField("Clinic ID")
    physician = models.IntegerField("Physician ID")
    patient = models.IntegerField("Patient ID")
    text = models.TextField("Text")