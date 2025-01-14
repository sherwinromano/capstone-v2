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
    RiskAssessment
)
from datetime import datetime

def is_admin(user):
    return user.is_staff

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Try to authenticate with username (student ID)
        user = authenticate(request, username=username, password=password)
        
        # If authentication fails, try with email
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            
            # Get or create student record
            try:
                student = Student.objects.get(student_id=user.username)
            except Student.DoesNotExist:
                # If student doesn't exist in main app, create it
                student = Student.objects.create(
                    user=user,
                    student_id=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email
                )

            # Check if patient profile exists
            try:
                patient = Patient.objects.get(student__student_id=user.username)
                return redirect('main:main')
            except Patient.DoesNotExist:
                # If no patient profile exists, redirect to patient form
                return redirect('main:patient_form')
        else:
            messages.error(request, 'Invalid ID number/Email or password')
            
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
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
        confirm_password = request.POST.get('confirmPassword')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('main:register')

        try:
            # Check if student_id or lrn already exists
            if Student.objects.filter(student_id=student_id).exists():
                messages.error(request, 'Student ID already exists')
                return redirect('main:register')
            
            if Student.objects.filter(lrn=lrn).exists():
                messages.error(request, 'LRN already exists')
                return redirect('main:register')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('main:register')

            # Create User account
            user = User.objects.create_user(
                username=student_id,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create Student profile with all required fields
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
                contact_number=''  # This field is required but can be updated later
            )

            messages.success(request, 'Registration successful! Please login.')
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
                student = Student.objects.get(student_id=request.user.username)
                return render(request, 'mainv2.html', {'student': student})
            except Student.DoesNotExist:
                messages.error(request, 'Student profile not found.')
                return redirect('main:login')
        # For staff/admin users
        else:
            return render(request, 'mainv2.html')
    return redirect('main:login')

@login_required
def patient_form_view(request):
    try:
        # Get the student instance using User's username (student_id)
        student = Student.objects.get(student_id=request.user.username)
        
        # Check if patient profile already exists
        existing_patient = Patient.objects.filter(student__student_id=student.student_id).exists()
        if existing_patient:
            return redirect('main:main')

    except Student.DoesNotExist:
        # Create student record if it doesn't exist
        student = Student.objects.create(
            user=request.user,
            student_id=request.user.username,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email
        )

    if request.method == 'POST':
        try:
            # Create physical examination record
            physical_exam = PhysicalExamination.objects.create(
                student=student
            )

            # Create patient record
            patient = Patient.objects.create(
                student=student,
                examination=physical_exam,
                birth_date=request.POST.get('birth_date'),
                age=calculate_age(request.POST.get('birth_date')),
                weight=float(request.POST.get('weight')),
                height=float(request.POST.get('height')),
                bloodtype=request.POST.get('bloodtype'),
                allergies=process_checkboxes(request.POST.getlist('allergies'), request.POST.get('other_allergies')),
                medications=request.POST.get('medications', 'None'),
                home_address=request.POST.get('home_address'),
                city=request.POST.get('city'),
                state_province=request.POST.get('state_province'),
                postal_zipcode=request.POST.get('postal_zipcode'),
                country=request.POST.get('country'),
                nationality=request.POST.get('nationality'),
                civil_status=request.POST.get('civil_status'),
                number_of_children=0,
                academic_year=f"{datetime.now().year}-{datetime.now().year + 1}",
                section="TBA",
                parent_guardian=request.POST.get('parent_guardian'),
                parent_guardian_contact_number=request.POST.get('parent_guardian_contact')
            )

            # Create medical history
            medical_history = MedicalHistory.objects.create(
                examination=physical_exam,
                tuberculosis='tuberculosis' in request.POST.getlist('medical_history', []),
                hypertension='hypertension' in request.POST.getlist('medical_history', []),
                heart_disease='heart_disease' in request.POST.getlist('medical_history', []),
                hernia='hernia' in request.POST.getlist('medical_history', []),
                epilepsy='epilepsy' in request.POST.getlist('medical_history', []),
                peptic_ulcer='peptic_ulcer' in request.POST.getlist('medical_history', []),
                kidney_disease='kidney_disease' in request.POST.getlist('medical_history', []),
                asthma='asthma' in request.POST.getlist('medical_history', []),
                insomnia='insomnia' in request.POST.getlist('medical_history', []),
                malaria='malaria' in request.POST.getlist('medical_history', []),
                venereal_disease='venereal_disease' in request.POST.getlist('medical_history', []),
                nervous_breakdown='nervous_breakdown' in request.POST.getlist('medical_history', []),
                jaundice='jaundice' in request.POST.getlist('medical_history', []),
                others=request.POST.get('other_medical', '')
            )

            # Create family history
            family_history = FamilyMedicalHistory.objects.create(
                examination=physical_exam,
                hypertension='hypertension' in request.POST.getlist('family_history', []),
                asthma='asthma' in request.POST.getlist('family_history', []),
                cancer='cancer' in request.POST.getlist('family_history', []),
                tuberculosis='tuberculosis' in request.POST.getlist('family_history', []),
                diabetes='diabetes' in request.POST.getlist('family_history', []),
                bleeding_disorder='bleeding_disorder' in request.POST.getlist('family_history', []),
                epilepsy='epilepsy' in request.POST.getlist('family_history', []),
                mental_disorder='mental_disorder' in request.POST.getlist('family_history', []),
                other_medical_history=request.POST.get('other_family_medical', '')
            )

            # Create risk assessment
            risk_assessment = RiskAssessment.objects.create(
                clearance=patient,
                age_above_60='age_above_60' in request.POST.getlist('risk_assessment', []),
                cardiovascular_disease='cardiovascular_disease' in request.POST.getlist('risk_assessment', []),
                chronic_lung_disease='chronic_lung_disease' in request.POST.getlist('risk_assessment', []),
                chronic_renal_disease='chronic_kidney_disease' in request.POST.getlist('risk_assessment', []),
                chronic_liver_disease='chronic_liver_disease' in request.POST.getlist('risk_assessment', []),
                cancer='cancer' in request.POST.getlist('risk_assessment', []),
                autoimmune_disease='autoimmune_disease' in request.POST.getlist('risk_assessment', []),
                pwd='pwd' in request.POST.getlist('risk_assessment', []),
                disability=request.POST.get('disability', '')
            )

            messages.success(request, 'Patient information saved successfully!')
            return redirect('main:main')

        except Exception as e:
            messages.error(request, f'Error saving patient information: {str(e)}')
            return render(request, 'patient_form.html')

    return render(request, 'patient_form.html')

def calculate_age(birthdate):
    born = datetime.strptime(birthdate, '%Y-%m-%d')
    today = datetime.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age

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
        student = Student.objects.get(student_id=request.user.username)
        patient = Patient.objects.filter(student=student).first()
        
        if patient:
            context = {
                'patient': patient,
                'medical_history': MedicalHistory.objects.filter(examination=patient.examination).first(),
                'family_history': FamilyMedicalHistory.objects.filter(examination=patient.examination).first(),
                'risk_assessment': RiskAssessment.objects.filter(clearance=patient).first(),
                'physical_exam': patient.examination,
            }
        else:
            context = {'patient': None}
            
    except Student.DoesNotExist:
        context = {'patient': None}
        messages.error(request, 'Student profile not found.')
        return redirect('main:login')

    return render(request, 'student_dashboard.html', context)