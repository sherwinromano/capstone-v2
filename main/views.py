from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StudentRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from medical.models import Patient, PatientRequest, EmergencyHealthAssistanceRecord, DentalRecords, MedicalCertificate, EligibilityForm
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.is_staff or user.is_superuser:
                    return redirect('main:admin_dashboard')
                else:
                    return redirect('main:main')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('main:main')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                print(f"Error during registration: {str(e)}")  # For debugging
        else:
            # Print form errors to console for debugging
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def recovery(request):
    return render(request, 'recovery.html')

def password_reset(request):
    return render(request, 'password-reset.html')

@login_required
def main_view(request):
    return render(request, 'mainv2.html')

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get counts for cards
    total_students = Patient.objects.count()
    total_medical_certs = MedicalCertificate.objects.count()
    total_dental_records = DentalRecords.objects.count()
    total_emergencies = EmergencyHealthAssistanceRecord.objects.count()
    
    # Get upcoming requests
    upcoming_requests = PatientRequest.objects.select_related(
        'patient', 
        'patient__student'
    ).filter(
        approve=False
    ).order_by('-date_requested')[:5]
    
    # Get upcoming appointments
    upcoming_schedules = DentalRecords.objects.select_related(
        'patient', 
        'patient__student'
    ).order_by('-date_appointed')[:5]

    context = {
        'total_students': total_students,
        'total_medical_certs': total_medical_certs,
        'total_dental_records': total_dental_records,
        'total_emergencies': total_emergencies,
        'upcoming_requests': upcoming_requests,
        'upcoming_schedules': upcoming_schedules,
    }
    
    return render(request, 'admin/dashboard.html', context)