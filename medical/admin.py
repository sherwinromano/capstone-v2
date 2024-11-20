from django.contrib import admin
from .models import (
    Student, 
    Patient,
    PhysicalExamination,
    MedicalClearance,
    RiskAssessment, 
    MedicalRequirement, 
    PatientRequest, 
    PrescriptionRecord, 
    TransactionRecord, 
    EmergencyHealthAssistanceRecord,
    MedicalHistory,
    FamilyMedicalHistory,
    ObgyneHistory,
    DentalRecords,
    MedicalClearance,
    EligibilityForm,
    MedicalCertificate
)

# Register your models here.

# class PatientAdmin(admin.ModelAdmin):
#     list_display = ['patient_id_number', 'full_name']

#     def full_name(self, obj):
#         return f"{obj.firstname} {obj.middlename} {obj.surname}"

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'lastname', 'firstname', 'middlename', 'sex')
    ordering = ('lastname',)

class DentalRecordsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service_type', 'date_requested', 'date_appointed')
    ordering = ('date_requested',)

class StudentRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'request_type', 'approve', 'date_requested', 'date_approved')
    ordering = ('date_requested',)

class EmergencyHealthAssistanceRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'reason', 'date_assisted')
    ordering = ('date_assisted',)

class PrescriptionRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'problem', 'treatment', 'date_prescribed')

class TransactionRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'transac_type', 'transac_date')

admin.site.register(Student, StudentAdmin)
admin.site.register(Patient)
admin.site.register(PhysicalExamination)
admin.site.register(MedicalClearance)
admin.site.register(RiskAssessment)
admin.site.register(MedicalRequirement)
admin.site.register(PatientRequest, StudentRequestAdmin)
admin.site.register(PrescriptionRecord, PrescriptionRecordAdmin)
admin.site.register(TransactionRecord, TransactionRecordAdmin)
admin.site.register(EmergencyHealthAssistanceRecord, EmergencyHealthAssistanceRecordAdmin)
admin.site.register(MedicalHistory)
admin.site.register(FamilyMedicalHistory)
admin.site.register(ObgyneHistory)
admin.site.register(DentalRecords, DentalRecordsAdmin)
admin.site.register(EligibilityForm)
admin.site.register(MedicalCertificate)