from django.contrib import admin

from .models import PatientProfile, Doctor

# Register your models here.
admin.site.register(Doctor)
admin.site.register(PatientProfile)
