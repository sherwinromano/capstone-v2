from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from main.models import Student
from medical.models import (
    PhysicalExamination,
    Patient,
    MedicalHistory,
    FamilyMedicalHistory,
    RiskAssessment,
    MentalHealthRecord
)
from datetime import datetime, date
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from medical import models as medical_models
from django.http import JsonResponse

def is_admin(user):
    return user.is_staff

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            
            redirect_url = 'main:main' if user.is_staff or user.is_superuser else 'main:patient_form'
            
            return JsonResponse({
                'status': 'success',
                'redirect_url': reverse(redirect_url)
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid ID number/Email or password'
            })

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('firstName')
            middle_initial = request.POST.get('middleInitial')
            last_name = request.POST.get('lastName')
            sex = request.POST.get('sex')
            year_level = request.POST.get('yrLevel')
            student_id = request.POST.get('idNumber')
            lrn = request.POST.get('lrn')
            degree = request.POST.get('course')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Create User account
            user = User.objects.create_user(
                username=student_id,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create Student in main app only
            Student.objects.create(
                student_id=student_id,
                lrn=lrn,
                lastname=last_name,
                firstname=first_name,
                middlename=middle_initial,
                degree=degree,
                year_level=int(year_level),
                sex=sex,
                email=email,
                contact_number=''
            )

            messages.success(request, 'Registration successful! Please complete your medical profile.')
            return redirect('main:login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('main:register')

    return render(request, 'register.html')

def recovery(request):
    return render(request, 'recovery.html')

def password_reset(request):
    return render(request, 'password-reset.html')


@login_required
def main_view(request):
    if request.user.is_authenticated:
        # For regular users (students)
        if not request.user.is_staff and not request.user.is_superuser:
            try:
                # Check medical student record
                medical_student = medical_models.Student.objects.get(student_id=request.user.username)
                
                # Check if student has completed medical profile
                try:
                    patient = medical_models.Patient.objects.get(student=medical_student)
                    # If patient record exists, show main dashboard
                    return render(request, 'mainv2.html', {'student': medical_student})
                except medical_models.Patient.DoesNotExist:
                    # If no patient record, redirect to patient form
                    messages.info(request, 'Please complete your medical profile first.')
                    return redirect('main:patient_form')
                    
            except medical_models.Student.DoesNotExist:
                messages.error(request, 'Student profile not found.')
                return redirect('main:login')
        # For staff/admin users
        else:
            return render(request, 'mainv2.html')
    return redirect('main:login')

@login_required
def patient_form(request):
    try:
        # Get the medical student instance
        medical_student = medical_models.Student.objects.get(student_id=request.user.username)
        
        if request.method == 'POST':
            # Create PhysicalExamination first
            physical_exam = medical_models.PhysicalExamination.objects.create(
                student=medical_student,
                date_of_physical_examination=timezone.now().strftime('%Y-%m-%d')
            )
            
            # Create Patient record
            patient = medical_models.Patient.objects.create(
                student=medical_student,
                birth_date=request.POST.get('birth_date'),
                age=calculate_age(request.POST.get('birth_date')),
                weight=float(request.POST.get('weight')),
                height=float(request.POST.get('height')),
                bloodtype=request.POST.get('bloodtype'),
                allergies=request.POST.get('allergies'),
                medications=request.POST.get('medications', 'None'),
                home_address=request.POST.get('home_address'),
                city=request.POST.get('city'),
                state_province=request.POST.get('state_province'),
                postal_zipcode=request.POST.get('postal_zipcode'),
                country=request.POST.get('country'),
                nationality=request.POST.get('nationality'),
                civil_status=request.POST.get('civil_status'),
                number_of_children=0,
                academic_year=f"{timezone.now().year}-{timezone.now().year + 1}",
                section=request.POST.get('section', 'TBA'),
                parent_guardian=request.POST.get('parent_guardian'),
                parent_guardian_contact_number=request.POST.get('parent_guardian_contact'),
                examination=physical_exam
            )
            
            # Create or update RiskAssessment record
            risk_assessment, created = medical_models.RiskAssessment.objects.update_or_create(
                clearance=patient,
                defaults={
                    'cardiovascular_disease': 'cardiovascular_disease' in request.POST,
                    'chronic_lung_disease': 'chronic_lung_disease' in request.POST,
                    'chronic_renal_disease': 'chronic_renal_disease' in request.POST,
                    'chronic_liver_disease': 'chronic_liver_disease' in request.POST,
                    'cancer': 'cancer' in request.POST,
                    'autoimmune_disease': 'autoimmune_disease' in request.POST,
                    'pwd': 'pwd' in request.POST,
                    'disability': request.POST.get('disability', '')
                }
            )
            
            messages.success(request, 'Medical information submitted successfully!')
            return redirect('main:student_dashboard')
            
    except medical_models.Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('main:login')
    except Exception as e:
        messages.error(request, f'Error saving patient information: {str(e)}')
        
    return render(request, 'patient_form.html')

def calculate_age(birthdate):
    born = datetime.strptime(birthdate, '%Y-%m-%d').date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def process_checkboxes(checkbox_list, other_value):
    if 'None' in checkbox_list:
        return 'None'
    result = ', '.join(filter(None, checkbox_list))
    if other_value:
        result = f"{result}, {other_value}" if result else other_value
    return result or 'None'

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    total_patients = Patient.objects.count()
    recent_examinations = PhysicalExamination.objects.order_by('-date_created')[:5]
    pending_clearances = Patient.objects.filter(riskassessment__isnull=True).count()

    # Add events data
    events = [
        {
            'date': '2025-01-13',
            'student': 'Test',
            'service': 'Cleaning'
        },
        {
            'date': '2025-01-13',
            'student': 'test',
            'service': 'Dental Filling'
        },
        {
            'date': '2025-01-20',
            'student': 'test',
            'service': 'Tooth Extraction'
        }
    ]
    
    context = {
        'total_patients': total_patients,
        'recent_examinations': recent_examinations,
        'pending_clearances': pending_clearances,
        'events': events
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def dashboard_view(request):
    try:
        # Get student by student_id (username)
        student = Student.objects.get(student_id=request.user.username)
        
        try:
            # Get the medical student instance
            medical_student = medical_models.Student.objects.get(student_id=student.student_id)
            patient = medical_models.Patient.objects.filter(student=medical_student).first()
            
            if patient:
                context = {
                    'student': student,
                    'patient': patient,
                    'medical_history': medical_models.MedicalHistory.objects.filter(examination=patient.examination).first(),
                    'family_history': medical_models.FamilyMedicalHistory.objects.filter(examination=patient.examination).first(),
                    'risk_assessment': medical_models.RiskAssessment.objects.filter(clearance=patient).first(),
                    'physical_exam': patient.examination,
                }
            else:
                context = {
                    'student': student,
                    'patient': None
                }
                messages.info(request, 'Please complete your medical profile.')
                return redirect('main:patient_form')
                
        except medical_models.Student.DoesNotExist:
            context = {
                'student': student,
                'patient': None
            }
            messages.error(request, 'Medical profile not found.')
            return redirect('main:patient_form')
            
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('main:login')

    return render(request, 'student_dashboard.html', context)

@user_passes_test(is_admin)
def mental_health_view(request):
    records = MentalHealthRecord.objects.all().order_by('-date_submitted')
    pending_count = records.filter(status='pending').count()
    
    context = {
        'records': records,
        'pending_count': pending_count,
    }
    return render(request, 'admin/mental_health.html', context)

@login_required
def mental_health_submit(request):
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(student__student_id=request.user.username)
            prescription = request.FILES.get('prescription')
            certification = request.FILES.get('certification')
            
            if not prescription or not certification:
                messages.error(request, 'Both prescription and certification are required.')
                return redirect('main:mental_health')
            
            MentalHealthRecord.objects.create(
                patient=patient,
                prescription=prescription,
                certification=certification
            )
            
            messages.success(request, 'Mental health documents submitted successfully.')
            return redirect('main:student_dashboard')
            
        except Patient.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return redirect('main:patient_form')
            
    return render(request, 'mental_health_submit.html')

@user_passes_test(is_admin)
def mental_health_review(request, record_id):
    record = get_object_or_404(MentalHealthRecord, id=record_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes')
        
        record.status = status
        record.notes = notes
        record.reviewed_by = request.user
        record.reviewed_at = timezone.now()
        record.save()
        
        # Send email notification to student
        subject = f'Mental Health Record Review - {status.title()}'
        message = f"""
        Dear {record.patient.student.firstname},
        
        Your mental health records have been reviewed.
        Status: {status.title()}
        
        Notes: {notes if notes else 'No additional notes.'}
        
        Best regards,
        Medical Services Team
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [record.patient.student.email],
            fail_silently=False,
        )
        
        messages.success(request, 'Record reviewed successfully.')
        return redirect('main:mental_health')
        
    return render(request, 'admin/mental_health_review.html', {'record': record})