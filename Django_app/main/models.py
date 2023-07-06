from django.db import models


class PatientProfile(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    email = models.EmailField()


class Doctor(models.Model):
    patient = models.ManyToManyField(PatientProfile)
    doctor = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default=1234)
    field_doctor = models.CharField(max_length=255)

    @staticmethod
    def get_customers_by_name(doctor):
        try:
            return Doctor.objects.get(doctor=doctor)
        except:
            return False


