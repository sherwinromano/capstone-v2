from django.urls import path
from . import views

app_name = 'medical'

urlpatterns = [
    path('patientbasicinfo/<int:student_id>/', views.patient_basic_info, name='patient_basicinfo'),
    path('medicalclearance/<int:student_id>/', views.medicalclearance_view, name='medicalclearance'),
    path('eligibilityform/<int:student_id>/', views.eligibilty_form, name='eligibility_form'),
    path('medicalcertificate/<int:student_id>/', views.med_cert, name='med_cert_for_intrams'),
    path('viewrequest/', views.view_request, name='viewrequest'),
    path('student/request/', views.submit_request, name="request"),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('physicalexam/<int:student_id>/', views.physical_examination, name='physical_exam'),
    path('medicalrequirementstracker/', views.student_medical_requirements_tracker, name='medtracker'),
    path('uploadrequirements/', views.upload_requirements, name='upload_requirements'),
    path('dentalservices/', views.dental_services, name='dentalservice'),
    path('dentalrequest/', views.dental_request, name='dentalrequest'),
    path('dentalschedule/', views.dental_schedule, name='dentalschedule'),
    path('listofpwd/', views.pwd_list, name='pwdlist'),
    path('pwd/<int:student_id>/', views.pwd_detail, name='pwd_detail'),
    path('prescriptions/', views.prescription, name='prescription'),
    path('prescriptionrecords/', views.view_prescription_records, name='prescription_records'),
    path('getstudentname/', views.get_student_name, name='get_student_name'),
    path('emergencyassistance/', views.emergency_asst, name='emergency_asst'),
    path('emergencyassistancerecords', views.view_emergency_health_records, name='emergency_health_records'),
    path('insuranceeligibility/', views.check_insurance_availability, name='insurance_eligibility'),
    # URL for the main transactions view
    path('transactions/', views.transactions_view, name='transactions'),
    path('monthly_transactions/', views.monthly_transactions_view, name='monthly_transactions'),
    path('daily_transactions/', views.daily_transactions_view, name='daily_transactions'),
    # path('yearly/', views.yearly_transactions, name='yearly_transactions'),
    path('upload/', views.upload_file, name='upload'),
]