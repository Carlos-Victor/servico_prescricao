from rest_framework import serializers

from prescription.models import Prescription



class GenericSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'id': instance
        }

class PrescriptionsSerializer(serializers.ModelSerializer):
    clinic = GenericSerializer()
    physician = GenericSerializer()
    patient = GenericSerializer()
    
    class Meta:
        model = Prescription
        fields = ('id','clinic', 'physician', 'patient', 'text', )