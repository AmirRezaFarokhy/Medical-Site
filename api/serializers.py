from rest_framework import serializers

from main.models import PatientProfile, Doctor

class SerializetionPatient(serializers.ModelSerializer):

    class Meta:
        model = PatientProfile
        fields = '__all__'



