from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from datetime import date
from django.utils import timezone
from datetime import timedelta  
from . models import(
    Patient,
    MedicalClearance,
    PhysicalExamination,
    RiskAssessment, 
    MedicalRequirement, 
    PatientRequest, 
    Student,
    TransactionRecord,
    MedicalHistory,
    FamilyMedicalHistory,
    ObgyneHistory,
    DentalRecords,
    EligibilityForm,
    EmergencyHealthAssistanceRecord,
    PrescriptionRecord,
    MedicalCertificate
)
from django.core.mail import send_mail
from django.conf import settings
import json
import calendar
import csv

from .forms import UploadFileForm

# Patient's basic information
def patient_basic_info(request, student_id):
    student = Student.objects.get(student_id=student_id)
    if Patient.objects.filter(student__student_id = student_id).exists():
        patient = Patient.objects.get(student__student_id = student_id)
        return render(request, "students/basicinfo.html", {"student": student, "patient": patient})
    if request.method == "POST":
        birth_date = request.POST.get("birth_date")
        age = request.POST.get("age")
        weight = request.POST.get("weight")
        height = request.POST.get("height")
        bloodtype = request.POST.get("bloodtype")
        allergies = request.POST.get("allergies")
        medications = request.POST.get("medications")
        home_address = request.POST.get("home_address")
        city = request.POST.get("city")
        state_province = request.POST.get("state-province")
        postal_zipcode = request.POST.get("postal-zip-code")
        country = request.POST.get("country")
        nationality = request.POST.get("nationality")
        civil_status = request.POST.get("civil_status")
        number_of_children = request.POST.get("number_of_children")
        academic_year = request.POST.get("academic_year")
        section = request.POST.get("section")
        parent_guardian = request.POST.get("parent_guardian")
        parent_guardian_contact_number = request.POST.get("parent_guardian_contact_number")

        Patient.objects.create(
            student = student,
            birth_date = birth_date,
            age = age,
            weight = weight,
            height = height,
            bloodtype = bloodtype,
            allergies = allergies,
            medications = medications,
            home_address = home_address,
            city = city,
            state_province = state_province,
            postal_zipcode = postal_zipcode,
            country = country,
            nationality = nationality,
            civil_status = civil_status,
            number_of_children = number_of_children,
            academic_year = academic_year,
            section = section,
            parent_guardian = parent_guardian,
            parent_guardian_contact_number = parent_guardian_contact_number
        )

        messages.success(request, "You may now do your transactions")
        return redirect("medical:request")
    return render(request, "students/basicinfo.html", {"student": student})

# view for handling clearance form submission
def medicalclearance_view(request, student_id):
    if request.user.is_superuser or request.user.is_staff:

        #if MedicalClearance.objects.filter(student__student_id = student_id).exists():
        #     clearance = MedicalClearance.objects.get(student__student_id = student_id)
        #    med_requirements = MedicalRequirement.objects.get(student__student_id = student_id)
        #     return render(request, "admin/patientclearance_comp.html", {"clearance":clearance, "med_requirements": med_requirements})
        patient = Patient.objects.get(student__student_id = student_id)
        if request.method == "POST":
            # Handle patient basic information
            age = request.POST.get("age")
            birth_date = request.POST.get("birth-date")
            street_address = request.POST.get("street-address")
            city = request.POST.get("city")
            state_province = request.POST.get("state-province")
            postal_zip_code = request.POST.get("postal-zip-code")
            country = request.POST.get("country")

            # student = Student.objects.get(student_id=student_id)
            # patient = Patient.objects.get(student__student_id = student_id)
            
            # Handle risk assessment 
            age_above_60 = request.POST.get("age_above_60") == "True"
            cardiovascular_disease = request.POST.get("cardiovascular-disease") == "True"
            chronic_lung_disease = request.POST.get("lung-disease") == "True"
            chronic_metabolic_disease = request.POST.get("diabetes") == "True"
            chronic_renal_disease = request.POST.get("renal-disease") == "True"
            chronic_liver_disease = request.POST.get("liver-disease") == "True"
            cancer = request.POST.get("cancer") == "True"
            autoimmune_disease = request.POST.get("autoimmune") == "True"
            pregnant = request.POST.get("pregnant") == "True"
            other_conditions = request.POST.get("other_conditions")
            living_with_vulnerable = request.POST.get("living_with_vulnerable") == "True"
            pwd = request.POST.get("pwd") == "True"
            disability = request.POST.get("disability_type")
            
            # Handles medical requirements 
            vaccination_type = request.POST.get("vaccination_type")
            vaccinated_1st = request.POST.get("vaccinated_1st", "off") == "on"
            vaccinated_2nd = request.POST.get("vaccinated_2nd", "off") == "on"
            vaccinated_booster = request.POST.get("vaccinated_booster", "off") == "on"

            x_ray_remarks = request.POST.get("x-ray-remark")
            cbc_remarks = request.POST.get("cbc-remark")
            drug_test_remarks = request.POST.get("drug-test-remark")
            stool_examination_remarks = request.POST.get("stool-examination-remark")
                
            # Insert medical requirements files
            try:
                med_requirements = MedicalRequirement.objects.get(patient__student__student_id = student_id)
                med_requirements.vaccination_type = vaccination_type
                med_requirements.vaccinated_1st = vaccinated_1st
                med_requirements.vaccinated_2nd = vaccinated_2nd
                med_requirements.vaccinated_booster = vaccinated_booster
                med_requirements.x_ray_remarks = x_ray_remarks
                med_requirements.cbc_remarks = cbc_remarks
                med_requirements.drug_test = drug_test_remarks
                med_requirements.stool_examination_remarks = stool_examination_remarks
                med_requirements.save()
            except MedicalRequirement.DoesNotExist:
                messages.error(request, "This patient doesn't have a medical requirements")
                return render(request, "admin/patientclearance_comp.html", {"patient":patient})

            if MedicalClearance.objects.filter(patient__student__student_id = student_id).exists():
                clearance = MedicalClearance.objects.get(patient__student__student_id = student_id)
                med_requirements = MedicalRequirement.objects.get(patient__student__student_id = student_id)

                clearance.patient.age = age
                clearance.patient.birth_date = birth_date
                clearance.patient.home_address = street_address
                clearance.patient.city = city
                clearance.patient.state_province = state_province
                clearance.patient.postal_zipcode = postal_zip_code
                clearance.patient.country = country
                

                # Update Risk Ass
                riskass = RiskAssessment.objects.get(clearance__patient__student__student_id = student_id)
                riskass.age_above_60 = age_above_60
                riskass.cardiovascular_disease = cardiovascular_disease
                riskass.chronic_lung_disease = chronic_lung_disease
                riskass.chronic_metabolic_disease = chronic_metabolic_disease
                riskass.chronic_renal_disease = chronic_renal_disease
                riskass.chronic_liver_disease = chronic_liver_disease
                riskass.cancer = cancer
                riskass.autoimmune_disease = autoimmune_disease
                riskass.pregnant = pregnant
                riskass.other_conditions = other_conditions
                riskass.living_with_vulnerable = living_with_vulnerable
                riskass.pwd = pwd
                riskass.disability = disability
                

                # Update Medical Requirements
                med_requirements_files = MedicalRequirement.objects.get(patient__student__student_id = student_id)
                med_requirements_files.vaccination_type = vaccination_type
                med_requirements_files.vaccinated_1st = vaccinated_1st
                med_requirements_files.vaccinated_2nd = vaccinated_2nd
                med_requirements_files.vaccinated_booster = vaccinated_booster
                med_requirements_files.x_ray_remarks = x_ray_remarks
                med_requirements_files.cbc_remarks = cbc_remarks
                med_requirements_files.drug_test_remarks = drug_test_remarks
                med_requirements_files.stool_examination_remarks = stool_examination_remarks
                
                # Save All
                clearance.save()
                riskass.save()
                med_requirements_files.save()
                messages.success(request, "Record Updated")
                return render(request, "admin/patientclearance_comp.html", {"patient": patient, "clearance":clearance, "med_requirements": med_requirements})
            
            # Create the clearance object
            # patient = Student.objects.get(student_id = student_id)
            clearance = MedicalClearance.objects.create(patient = patient)

            # The risk assessment
            rsk = RiskAssessment.objects.create(
                    clearance = clearance, 
                    age_above_60 = age_above_60, 
                    cardiovascular_disease = cardiovascular_disease,
                    chronic_lung_disease = chronic_lung_disease, 
                    chronic_metabolic_disease = chronic_metabolic_disease,
                    chronic_renal_disease = chronic_renal_disease, 
                    chronic_liver_disease = chronic_liver_disease,
                    cancer = cancer, 
                    autoimmune_disease = autoimmune_disease, 
                    pregnant = pregnant, 
                    other_conditions = other_conditions, 
                    living_with_vulnerable = living_with_vulnerable,
                    pwd = pwd
                )
            # Handle if pwd
            if pwd:
                rsk.disability = disability
                rsk.save()

            # Record requests
            # patient_request = PatientRequest.objects.get(patient__student__student_id = student_id, request_type = "Medical Clearance for OJT/Practicum")
        
            # patient_request.save()

            messages.success(request, "Medical Clearance created successfully.")
            return render(request, "admin/patientclearance_comp.html", {"patient": patient, "clearance":clearance, "med_requirements": med_requirements})
        #student = Student.objects.get(student_id=student_id)

        if MedicalClearance.objects.filter(patient__student__student_id = student_id).exists():
            clearance = MedicalClearance.objects.get(patient__student__student_id = student_id)
            med_requirements = MedicalRequirement.objects.get(patient__student__student_id = student_id)
            return render(request, "admin/patientclearance_comp.html", {"patient": patient, "clearance": clearance, "med_requirements": med_requirements})
        messages.info(request, f"Fill out the necessary information to complete {patient.student.firstname.title()}'s Medical Clearance.")
        return render(request, "admin/patientclearance_comp.html", {"patient":patient})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

# Views for handling eligibilty form creation
def eligibilty_form(request, student_id):
    if request.user.is_superuser or request.user.is_staff:
        # if EligibilityForm.objects.filter(student__student_id = student_id).exists():
        #     student_eligibilty_form = EligibilityForm.objects.get(student__student_id = student_id)
        #     return render(request, "admin/eligibilityformcomp.html", {"eligibility_form": student_eligibilty_form})

        #student = Student.objects.get(student_id=student_id)
        patient = Patient.objects.get(student__student_id=student_id)
        # Get data inputted from eligibility form
        if request.method == "POST":
            age = request.POST.get("age")
            birth_date = request.POST.get("birth-date")
            weight = request.POST.get("weight")
            height = request.POST.get("height")
            blood_type = request.POST.get("blood-type")
            allergies = request.POST.get("allergies")
            medications = request.POST.get("medication")
            address = request.POST.get("address")
            competetions = request.POST.get("competition")
            date_event = request.POST.get("date-event")
            venue = request.POST.get("place-event")
            blood_pressure = request.POST.get("blood-pressure")
            date_of_examination = request.POST.get("date-exam")
            license_number = request.POST.get("liscence-number")
            validity_date = request.POST.get("validity-date")

            if EligibilityForm.objects.filter(patient__student__student_id = student_id).exists():
                patient_eligibilty_form = EligibilityForm.objects.get(patient__student__student_id = student_id)

                patient_eligibilty_form.patient.age = age
                patient_eligibilty_form.patient.birth_date = birth_date
                patient_eligibilty_form.patient.weight = weight
                patient_eligibilty_form.patient.height = height
                patient_eligibilty_form.patient.bloodtype = blood_type
                patient_eligibilty_form.patient.allergies = allergies
                patient_eligibilty_form.patient.medications = medications
                patient_eligibilty_form.patient.home_address = address
                patient_eligibilty_form.blood_pressure = blood_pressure
                patient_eligibilty_form.date_of_event = date_event
                patient_eligibilty_form.competetions = competetions,
                patient_eligibilty_form.venue = venue
                patient_eligibilty_form.date_of_examination = date_of_examination
                patient_eligibilty_form.liscence_number = license_number
                patient_eligibilty_form.validity_date = validity_date

                patient_eligibilty_form.save()
                messages.success(request, "Record Updated")
                return render(request, "admin/eligibilityformcomp.html", {"patient": patient, "eligibility_form": patient_eligibilty_form})

            # If not exists
            patient_eligibilty_form = EligibilityForm.objects.create(
                patient = patient,
                blood_pressure = blood_pressure,
                competetions = competetions,
                date_of_event = date_event,
                venue = venue,
                date_of_examination = date_of_examination,
                liscence_number = license_number,
                validity_date = validity_date
            )
            
            # patient_request = PatientRequest.objects.get(patient__student__student_id = student_id, request_type = "Eligibility Form")
            # student_request.date_approved = datetime.now()
            # student_request.save()

            messages.success(request, "Eligibility Form successfully created")
            return render(request, "admin/eligibilityformcomp.html", {"patient": patient, "eligibility_form": patient_eligibilty_form})      
        
        if EligibilityForm.objects.filter(patient__student__student_id = student_id).exists():
            patient_eligibilty_form = EligibilityForm.objects.get(patient__student__student_id = student_id)
            return render(request, "admin/eligibilityformcomp.html", {"patient": patient, "eligibility_form": patient_eligibilty_form})
        
        messages.info(request, f"Fill out the necessary information to complete {patient.student.firstname.title()}'s Eligibility Form.")
        return render(request, "admin/eligibilityformcomp.html", {"patient": patient})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
# List of student for patient profile
def patient_profile(request):
    if request.user.is_superuser or request.user.is_staff:
        patients = Patient.objects.all().order_by('student__lastname')
        if request.method == "POST":
            student_id = request.POST.get("student_id")
            try:
                patient = Patient.objects.filter(student__student_id = student_id)
                return render(request, "admin/patientprofile.html", {"patients": patient})
            except Student.DoesNotExist:
                return render(request, "admin/patientprofile.html", {"patients": patients})
        return render(request, "admin/patientprofile.html", {"patients": patients})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

# View students request, eg. Medical Clearance for OJT/Practicum, Eligibility Form and Medical Certificate
def view_request(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    patient_requests = PatientRequest.objects.all()
    
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        request_type = request.POST.get("request_type")
        action = request.POST.get("action")
        
        patient_request = get_object_or_404(PatientRequest, request_id=request_id, request_type=request_type)
        
        try:
            if action == "approve":
                patient_request.approve = True
                patient_request.date_approved = datetime.now()
                patient_request.save()
                messages.success(request, "Marked as approved")
                
                # Send approval email
                patient = patient_request.patient.student
                patient_name = f"{patient.firstname} {patient.lastname}"
                patient_email = patient.email
                
                # Construct approval email body using HTML template
                approval_email_subject = 'Your Document Request Has Been Approved'
                approval_email_body = f"""
                    <html>
                    <body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
                        <div style='max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9;'>
                            <h2 style='text-align: center; color: #0056b3;'>REQUEST APPROVAL</h2>
                            <p>Dear <strong>{patient_name}</strong>,</p>
                            <p>We're pleased to inform you that your document request for <strong>'{request_type}'</strong> has been <strong style='color:green;'>APPROVED</strong>.</p>
                            <p>Please proceed to the Kahimsug Clinic for the necessary examination and to claim the printed copy of your document.</p>
                            <p>Best Regards,</p>
                            <p><strong>CTU - Argao Campus Kahimsug Clinic</strong></p>
                        </div>
                    </body>
                    </html>
                """
                
                send_mail(
                    approval_email_subject,
                    '',
                    settings.EMAIL_HOST_USER,
                    [patient_email],
                    html_message=approval_email_body,  # Send email as HTML
                    fail_silently=False,
                )
                
            elif action == "reject":
                patient_request.delete()
                messages.error(request, "Request rejected")
                
                # Send rejection email
                patient = patient_request.patient.student
                patient_name = f"{patient.firstname} {patient.lastname}"
                patient_email = patient.email
                
                # Construct rejection email body using HTML template
                rejection_email_subject = 'Your Document Request Has Been Rejected'
                rejection_email_body = f"""
                    <html>
                    <body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
                        <div style='max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9;'>
                            <h2 style='text-align: center; color: #d9534f;'>REQUEST REJECTION</h2>
                            <p>Dear <strong>{patient_name}</strong>,</p>
                            <p>We regret to inform you that your document request for <strong>'{request_type}'</strong> has been <strong style='color:red;'>REJECTED</strong>.</p>
                            <p>Please review the requirements and resubmit your request if necessary.</p>
                            <p>Best Regards,</p>
                            <p><strong>CTU - Argao Campus Kahimsug Clinic</strong></p>
                        </div>
                    </body>
                    </html>
                """
                
                send_mail(
                    rejection_email_subject,
                    '',
                    settings.EMAIL_HOST_USER,
                    [patient_email],
                    html_message=rejection_email_body,  # Send email as HTML
                    fail_silently=False,
                )
                
            elif action == "done":
                # Create a transaction record
                TransactionRecord.objects.create(
                    patient=patient_request.patient,
                    transac_type="Medical Document Request",
                    transac_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                patient_request.delete()
                messages.success(request, "Transaction successfully completed")
        except PatientRequest.DoesNotExist:
            messages.error(request, "Something went wrong")
    
    return render(request, "admin/viewrequest.html", {"patient_requests": patient_requests})

# Views for creating Physical Examintaion Reports
def physical_examination(request, student_id):
    if request.user.is_superuser or request.user.is_staff:
        patient = Patient.objects.get(student__student_id=student_id)

        # if PhysicalExamination.objects.filter(student__student_id=student_id).exists():
        #     examination = PhysicalExamination.objects.get(student__student_id=student_id)
        #     return render(request, "admin/physicalexamcomp.html", {"examination": examination, "students": student})
        
        if request.method == "POST":
            # Get patient basic information
            # date_exam = request.POST.get("date")
            # date_of_physical_examination = datetime.strptime(str_date_exam, "%Y-%m-%d")
            # birthdate = request.POST.get("birth_date")
            # birth_date = datetime.strptime(str_birthdate, "%Y-%m-%d")
            birth_date = request.POST.get("birth_date")
            date_of_physical_examination = request.POST.get("date")
            address = request.POST.get("home_address")
            age = request.POST.get("age")
            nationality = request.POST.get("nationality")
            civil_status = request.POST.get("civil_status")
            number_of_children = request.POST.get("number_of_children", 0)
            academic_year = request.POST.get("academic_year")
            section = request.POST.get("academic_year")
            parent_guardian = request.POST.get("parent_guardian")
            parent_contact = request.POST.get("parent_guardian_contact_number")
            
            # Get patient medical history
            tuberculosis = request.POST.get("tuberculosis") == "on"
            peptic_ulcer = request.POST.get("peptic-ulcer") == "on"
            venereal = request.POST.get("venereal-disease") == "on"
            hypertension = request.POST.get("hypertension") == "on"
            kidney_disease = request.POST.get("kidney-disease") == "on"
            allergic_reaction = request.POST.get("allergic-reaction") == "on"
            heart_disease = request.POST.get("heart-diseases") == "on"
            asthma = request.POST.get("asthma") == "on"
            nervous_breakdown = request.POST.get("nervous-breakdown") == "on"
            hernia = request.POST.get("hernia") == "on"
            insomnia = request.POST.get("insomnia") == "on"
            jaundice = request.POST.get("jaundice") == "on"
            epilepsy = request.POST.get("epilepsy") == "on"
            malaria = request.POST.get("malaria") == "on"
            others = request.POST.get("others")
            no_history = request.POST.get("none") == "on"
            hospital_admission = request.POST.get("operations")
            medications = request.POST.get("medications")

            # Get patient's family medical history
            hypertension_family = request.POST.get("hypertension-family") == "on"
            tuberculosis_family = request.POST.get("tuberculosis-family") == "on"
            asthma_family = request.POST.get("asthma-family") == "on"
            diabetes = request.POST.get("diabetes") == "on"
            cancer = request.POST.get("cancer") == "on"
            bleeding_disorder = request.POST.get("bleeding-disorder") == "on"
            epilepsy_family = request.POST.get("epilepsy-family") == "on"
            mental_disorders = request.POST.get("mental-disorders") == "on"
            family_others = request.POST.get("family-others")
            family_no_history = request.POST.get("no_history") == "on"

            # Get OB-GYNE history
            menarche = request.POST.get("menarche")
            lmp = request.POST.get("lmp")
            gravida = request.POST.get("gravida")
            para = request.POST.get("para")
            menopause = request.POST.get("menopause")
            pap_smear = request.POST.get("pap_swear")
            additional_history = request.POST.get("additional-history")

            # Check if object already exists
            if PhysicalExamination.objects.filter(patient__student__student_id=student_id).exists():
                examination = PhysicalExamination.objects.get(patient__student__student_id=student_id)

                # Update Physical Examination
                # birth_date = datetime.strptime(str_birthdate, "%B %d, %Y")
                examination.patient.birth_date = birth_date
                examination.patient.home_address = address
                examination.patient.age = age
                examination.patient.nationality = nationality
                examination.patient.civil_status = civil_status
                examination.patient.number_of_children = number_of_children
                examination.patient.academic_year = academic_year
                examination.patient.section = section
                # date_of_physical_examination = datetime.strptime(str_date_exam, "%B %d, %Y")
                examination.date_of_physical_examination = date_of_physical_examination
                examination.patient.parent_guardian = parent_guardian
                examination.patient.parent_guardian_contact_number = parent_contact
                # Save
                examination.save()

                # Update Medical History
                medical_history = MedicalHistory.objects.get(examination__patient__student__student_id = student_id)
                medical_history.tuberculosis = tuberculosis
                medical_history.hypertension = hypertension
                medical_history.heart_disease = heart_disease
                medical_history.hernia = hernia
                medical_history.epilepsy = epilepsy
                medical_history.peptic_ulcer = peptic_ulcer
                medical_history.kidney_disease = kidney_disease
                medical_history.asthma = asthma
                medical_history.insomnia = insomnia
                medical_history.malaria = malaria
                medical_history.venereal_disease = venereal
                medical_history.allergic_reaction = allergic_reaction
                medical_history.nervous_breakdown = nervous_breakdown
                medical_history.jaundice = jaundice
                medical_history.others = others
                medical_history.no_history = no_history
                medical_history.hospital_admission = hospital_admission
                medical_history.medications = medications
                # Save
                medical_history.save()

                # Update Family History
                family_history = FamilyMedicalHistory.objects.get(examination__patient__student__student_id = student_id)
                family_history.hypertension = hypertension_family
                family_history.asthma = asthma_family
                family_history.cancer = cancer
                family_history.tuberculosis = tuberculosis_family
                family_history.diabetes = diabetes
                family_history.bleeding_disorder = bleeding_disorder
                family_history.epilepsy = epilepsy_family
                family_history.mental_disorder = mental_disorders
                family_history.no_history = family_no_history
                family_history.other_medical_history = family_others
                # Save
                family_history.save()

                # ObgyneHistory
                obgyne = ObgyneHistory.objects.get(examination__patient__student__student_id = student_id)
                obgyne.menarche = menarche
                obgyne.lmp = lmp
                obgyne.pap_smear = pap_smear
                obgyne.gravida = gravida
                obgyne.para = para
                obgyne.menopause = menopause
                obgyne.additional_history = additional_history
                # Save
                obgyne.save()
                messages.success(request, "Record Updated")
                return render(request, "admin/physicalexamcomp.html", {"examination": examination, "patient": patient})
        
            # Create the physical examination object if it does not exists
            # examination = PhysicalExamination.objects.get(student_id = student_id)
            examination = PhysicalExamination.objects.create(
                patient = patient,
                date_of_physical_examination = date_of_physical_examination,
                # birth_date = birth_date,
                # address = address,
                # age = age,
                # nationality = nationality,
                # civil_status = civil_status,
                # number_of_children = number_of_children,
                # academic_year = academic_year,
                # section = section,
                # parent_guardian = parent_guardian,
                # parent_guardian_contact_number = parent_contact
            )

            # Insert data into the medical history of the patients model
            MedicalHistory.objects.create(
                examination = examination,
                tuberculosis = tuberculosis,
                hypertension = hypertension,
                heart_disease = heart_disease,
                hernia = hernia,
                epilepsy = epilepsy,
                peptic_ulcer = peptic_ulcer,
                kidney_disease = kidney_disease,
                asthma = asthma,
                insomnia = insomnia,
                malaria = malaria,
                venereal_disease = venereal,
                allergic_reaction = allergic_reaction,
                nervous_breakdown = nervous_breakdown,
                jaundice = jaundice,
                others = others,
                no_history = no_history,
                hospital_admission = hospital_admission,
                medications = medications
            )

            # Insert to patient's family's medical history
            FamilyMedicalHistory.objects.create(
                examination = examination,
                hypertension = hypertension_family,
                asthma = asthma_family,
                cancer = cancer,
                tuberculosis = tuberculosis_family,
                diabetes = diabetes,
                bleeding_disorder = bleeding_disorder,
                epilepsy = epilepsy_family,
                mental_disorder = mental_disorders,
                no_history = family_no_history,
                other_medical_history = family_others
            )

            # Insert to OB-GYNE models
            ob = ObgyneHistory.objects.create(
                examination = examination,
                menarche = menarche,
                lmp = lmp,
                pap_smear = pap_smear,
                gravida = gravida,
                para = para,
                menopause = menopause,
                additional_history = additional_history
            )

            messages.success(request, "Physical Examination Done!")
            # record_transaction(patient, "Physical Examination")
            return render(request, "admin/physicalexamcomp.html", {"examination": examination, "patient": patient})
        
        if PhysicalExamination.objects.filter(patient__student__student_id=student_id).exists():
            examination = PhysicalExamination.objects.get(patient__student__student_id=student_id)
            return render(request, "admin/physicalexamcomp.html", {"examination": examination, "patient": patient})
        
        messages.info(request, f"Fill out the necessary information to complete {patient.student.firstname.title()}'s Physical Examination.")
        return render(request, "admin/physicalexamcomp.html", {"patient": patient})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

# Record prescriptions
def prescription(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == "POST":
            student_id = request.POST.get("student_id")
            name = request.POST.get("name")
            problem = request.POST.get("problem")
            treatment = request.POST.get("treatment")
            str_date_prescribed = request.POST.get("date_prescribed")
            date_prescribed = datetime.strptime(str_date_prescribed, "%Y-%m-%d")

            # Validate student existence
            try:
                patient = Patient.objects.get(student__student_id=student_id)
            except Patient.DoesNotExist:
                messages.info(request, "Fill out this form first to record patient's basic information.")
                return redirect('medical:patient_basicinfo', student_id)

            # Retrieve student associated with the patient
            student = get_object_or_404(Student, student_id=student_id)
            full_name = f"{student.firstname} {student.lastname}"

            # Validate inputted name against student's name (case-insensitive)
            if name.lower() != full_name.lower():
                messages.error(request, "The entered name does not match the student's name associated with the inputted student ID.")
                return render(request, "admin/prescription.html", {})

            # Create prescription record
            PrescriptionRecord.objects.create(
                patient=patient,
                name=name,
                problem=problem,
                treatment=treatment,
                date_prescribed=date_prescribed
            )

            messages.success(request, "Record Saved")
            record_transaction(patient, "Prescription Issuance")
            return render(request, "admin/prescription.html", {})
        else:
            return render(request, "admin/prescription.html", {})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

def get_student_name(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")

        try:
            student = Student.objects.get(student_id=student_id)
            student_name = f"{student.firstname} {student.lastname}".title()
            print(student_name)
            return JsonResponse({"student_name": student_name})
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)

#check if student matched
# def check_student_match(request):
#     if request.method == "GET":
#         student_id = request.GET.get("student_id")
#         name = request.GET.get("name")

#         try:
#             student = Student.objects.get(student_id=student_id)
#             student_name = f"{student.firstname} {student.lastname}"

#             # Check if the provided name matches the student name associated with the student ID
#             if name.lower() == student_name.lower():
#                 return JsonResponse({'success': True})
#             else:
#                 return JsonResponse({'success': False, 'message': 'Student name does not match the provided name'})
#         except Student.DoesNotExist:
#             return JsonResponse({'success': False, 'message': 'Student with the provided ID does not exist'})   

# Record Emergency Health Assistance
def emergency_asst(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == "POST":
            student_id = request.POST.get("student_id")
            # patient = Patient.objects.get(student__student_id=student_id)
            name = request.POST.get("name")
            reason = request.POST.get("problem")
            str_date_assisted = request.POST.get("date_assisted")
            date_assisted = datetime.strptime(str_date_assisted, "%Y-%m-%d")

            try:
                # Retrieve the patient information based on the student ID
                patient = Patient.objects.get(student__student_id=student_id)
                # Convert both names to lowercase for case-insensitive comparison
                inputted_name_lower = name.lower()
                student_name_lower = f"{patient.student.firstname} {patient.student.lastname}".lower()
                # Validate if the inputted name matches the first name and last name of the patient
                if inputted_name_lower != student_name_lower:
                    messages.error(request, "The entered name does not match the student's name associated with the inputted student ID.")
                    return redirect('medical:emergency_asst')  # Redirect to the same page
            except Patient.DoesNotExist:
                messages.info(request, "Fill out this form first to record patient's basic information")
                return redirect('medical:patient_basicinfo', student_id)
            
            # Create EmergencyHealthAssistanceRecord
            EmergencyHealthAssistanceRecord.objects.create(
                name=name,
                patient=patient,
                reason=reason,
                date_assisted=date_assisted
            )
            messages.success(request, "Record Saved")
            # Record transaction
            record_transaction(patient, "Emergency Health Assistance")
            return render(request, "admin/emergency_asst.html", {"student_name": {}})
            #return redirect('medical:emergency_asst')  # Redirect to the same page after successful record creation
        
        return render(request, "admin/emergency_asst.html", {})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
def record_transaction(patient, transac_type):
    TransactionRecord.objects.create(
        patient = patient, 
        transac_type = transac_type, 
        transac_date = datetime.now()
    )

# Record students request eg. Medical Clearance for OJT/Practicum, Eligibility Form and Medical Certificate
def submit_request(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        valid_id = Student.objects.filter(student_id=student_id).exists()
        if not valid_id:
            messages.error(request, "The ID you entered does not exist.")
            return render(request, "students/requestform.html", {})
        
        student = Student.objects.get(student_id=student_id)
        # Check if student already in the patients database
        if not Patient.objects.filter(student__student_id = student_id).exists():
            messages.info(request, "Fill out this form first before doing any transactions")
            return redirect('medical:patient_basicinfo', student_id)
            #return render(request, "students/basicinfo.html", {"student": student})
        
        request_type = request.POST.get("request_type")
        
        if PatientRequest.objects.filter(patient__student__student_id=student_id, request_type=request_type).exists():
            messages.error(request, "You have already submitted this type of request")
            return render(request, "students/requestform.html", {})
        
        patient = Patient.objects.get(student__student_id=student_id)
        transac_type = f"Request for {request_type}"
        
        # Create the student request object
        patient_request = PatientRequest.objects.create(
            patient=patient,
            request_type=request_type,
            date_requested=datetime.now()
        )

        # Send confirmation email to the student
        patient_name = f"{patient.student.firstname} {patient.student.lastname}"
        patient_email = patient.student.email
        email_subject = 'Request Confirmation'
        email_body = f"""
        <html>
        <body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
            <div style='max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9;'>
                <h2 style='text-align: center; color: #0056b3;'>REQUEST CONFIRMATION</h2>
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>Thank you for submitting your request for the document <strong>'{request_type}'</strong>. We have received it and our team is now processing it with utmost care and attention.</p>
                <p>Your request is currently being evaluated by our clinic nurse. You will receive another email once your document is approved.</p>
                <p>If you have any questions or need further assistance, feel free to reply to this email or contact our support team at support@example.com.</p>
                <p>Best Regards,</p>
                <p><strong>CTU - Argao Campus Kahimsug Clinic Team</strong></p>
            </div>
        </body>
        </html>
        """

        send_mail(
            email_subject,
            '',
            settings.EMAIL_HOST_USER,
            [patient_email],
            html_message=email_body,
            fail_silently=False,
        )

        messages.success(request, "Request submitted. A confirmation email has been sent.")
        # record_transaction(patient, transac_type)
        return render(request, "students/requestform.html", {})
    return render(request, "students/requestform.html", {})

# Views for medical requirements tracker
def student_medical_requirements_tracker(request):
     if request.method == "POST":
        student_id = request.POST.get("student_id")
        patient = Patient.objects.filter(student__student_id = student_id).exists()
        if not patient:
            messages.error(request, "The student ID you entered does not exists")
            return render(request, "medicalrequirements.html", {})
        # if not MedicalRequirement.objects.filter(clearance__student__student_id = student_id).exists():
        #     messages.error(request, "This student did not upload any requirements")
        #     return render(request, "medicalrequirements.html", {})
        try:
            med_requirements = MedicalRequirement.objects.get(patient__student__student_id = student_id)
            print(med_requirements.cbc.url)
        except MedicalRequirement.DoesNotExist:
            messages.error(request, "This student did not upload any requirements")
            return render(request, "medicalrequirements.html", {})
        return render(request, "medicalrequirements.html", {"med_requirements": med_requirements})
     return render(request, "medicalrequirements.html", {})

# Views for handling the medical requirements uploaded file
def upload_requirements(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        try:
            patient = Patient.objects.get(student__student_id=student_id)
        except Patient.DoesNotExist:
            # If patient does not exist, redirect to basicinfo.html
            messages.info(request, "Fill out this form first before doing any transactions")
            return redirect('medical:patient_basicinfo', student_id=student_id)

        x_ray = request.FILES.get("x-ray")
        cbc = request.FILES.get("cbc")
        drug_test = request.FILES.get("drug-test")
        stool_exam = request.FILES.get("stool-exam")
        pwd_card = request.FILES.get("pwd-card")

        # Check if file is less than 5 MB, pwd card excluded
        if (x_ray and (x_ray.size / 1_048_576) > 5) or (cbc and (cbc.size / 1_048_576) > 5) or (stool_exam and (stool_exam.size / 1_048_576) > 5) or (drug_test and (drug_test.size / 1_048_576) > 5):
            messages.error(request, "File size exceeds the limit.")
            return render(request, "students/medupload.html", {"patient": patient})

        # Check if the medical requirements already exist
        try:
            md = MedicalRequirement.objects.get(patient=patient)

            # Update existing records
            if x_ray:
                md.chest_xray.save(x_ray.name, x_ray)
            if cbc:
                md.cbc.save(cbc.name, cbc)
            if drug_test:
                md.drug_test.save(drug_test.name, drug_test)
            if stool_exam:
                md.stool_examination.save(stool_exam.name, stool_exam)
            if pwd_card:
                md.pwd_card.save(pwd_card.name, pwd_card)

            md.save()
            messages.success(request, "Your files have been successfully updated")
        except MedicalRequirement.DoesNotExist:
            # Create new records
            md = MedicalRequirement.objects.create(
                patient=patient,
                chest_xray=x_ray,
                cbc=cbc,
                drug_test=drug_test,
                stool_examination=stool_exam
            )
            if pwd_card:
                md.pwd_card.save(pwd_card.name, pwd_card)

            messages.success(request, "Your files have been successfully uploaded")

        return render(request, "students/medupload.html", {"patient": patient, "md": md})

    # GET request
    if request.method == "GET":
        student_id = request.GET.get("student_id")
        if student_id:
            try:
                patient = Patient.objects.get(student__student_id=student_id)
                md = MedicalRequirement.objects.get(patient=patient)
                return render(request, "students/medupload.html", {"patient": patient, "md": md})
            except Patient.DoesNotExist:
                # If patient does not exist, redirect to basicinfo.html
                messages.info(request, "Fill out this form first before doing any transactions")
                return redirect('medical:patient_basicinfo', student_id=student_id)
            except MedicalRequirement.DoesNotExist:
                return render(request, "students/medupload.html", {"patient": patient})

    return render(request, "students/medupload.html", {})
# Views for handling students request for dental services
def dental_services(request):
    if request.method == "POST":
        transac_type = ""
        student_id = request.POST.get("student_id")
        service_type = request.POST.get("service_type")

        valid_id = Student.objects.filter(student_id=student_id).exists()
        if not valid_id:
            messages.error(request, "The ID you entered does not exist.")
            return render(request, "students/dentalrequestform.html", {})
        
        if not Patient.objects.filter(student__student_id = student_id).exists():
            messages.info(request, "Fill out this form first before doing any transactions")
            return redirect('medical:patient_basicinfo', student_id)
            #return render(request, "students/basicinfo.html", {"student": student})
        
        dental_service_request = DentalRecords.objects.filter(patient__student__student_id=student_id, service_type=service_type)
        if dental_service_request.exists():
            messages.error(request, "You have already requested this type of service")
            return render(request, "students/dentalrequestform.html", {})
        
        patient = Patient.objects.get(student__student_id=student_id)
        transac_type = f"Request for dental {service_type}"
        
        # Create dental service request object
        dental_request = DentalRecords.objects.create(
            patient=patient,
            service_type=service_type,
            date_requested=datetime.now()
        )

        # Send confirmation email to the student
        patient_name = f"{patient.student.firstname} {patient.student.lastname}"
        patient_email = patient.student.email
        email_subject = 'Dental Services Request Submitted'
        email_body = f"""
        <html>
        <body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
            <div style='max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9;'>
                <h2 style='text-align: center; color: #0056b3;'>Dental Services Request Submitted</h2>
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>Your request for dental service <strong>{service_type}</strong> has been successfully submitted.</p>
                <p>Please wait for another email with the appointment schedule.</p>
                <p>Best Regards,</p>
                <p><strong>CTU - Argao Campus Kahimsug Clinic</strong></p>
            </div>
        </body>
        </html>
        """

        send_mail(
            email_subject,
            '',
            settings.EMAIL_HOST_USER,
            [patient_email],
            html_message=email_body,
            fail_silently=False,
        )

        messages.success(request, "Request submitted. A confirmation email has been sent.")
        # record_transaction(patient, transac_type)
        return render(request, "students/dentalrequestform.html", {})
    
    return render(request, "students/dentalrequestform.html", {})

# Views for appointing students dental requests
def dental_request(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to access this page.")

    service_request = DentalRecords.objects.all()

    if request.method == "POST":
        try:
            request_id = request.POST.get("request_id")
            patient_dental_request = DentalRecords.objects.get(id=request_id)
            str_appointment_date = request.POST.get("appointment_date")
            str_appointment_time = request.POST.get("appointment_time")
            
            if not str_appointment_date or not str_appointment_time:
                raise ValueError("Appointment date and time are required")

            # Combine date and time strings into a datetime object
            appointment_datetime = datetime.strptime(f"{str_appointment_date} {str_appointment_time}", "%Y-%m-%d %H:%M")

            # Convert appointment datetime to the current timezone
            appointment_datetime = timezone.make_aware(appointment_datetime)

            patient_dental_request.date_appointed = appointment_datetime
            patient_dental_request.appointed = True
            patient_dental_request.save()

            # Send confirmation email to the student
            patient = patient_dental_request.patient
            patient_name = f"{patient.student.firstname} {patient.student.lastname}"
            patient_email = patient.student.email
            service_type = patient_dental_request.service_type

            email_subject = f'Dental Appointment Scheduled'
            email_body = f"""
            <html>
            <body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
                <div style='max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9;'>
                    <h2 style='text-align: center; color: #0056b3;'>Appointment Date Set</h2>
                    <p>Dear <strong>{patient_name}</strong>,</p>
                    <p>We're pleased to inform you that your appointment date has been set for {appointment_datetime.strftime("%B %d, %Y")} at {appointment_datetime.strftime("%I:%M %p")}.</p>
                    <p>Please make sure to attend the appointment on time.</p>
                    <p>Best Regards,</p>
                    <p><strong>CTU - Argao Campus Kahimsug Clinic</strong></p>
                </div>
            </body>
            </html>
            """

            send_mail(
                email_subject,
                '',
                settings.EMAIL_HOST_USER,
                [patient_email],
                html_message=email_body,
                fail_silently=False,
            )

            messages.success(request, "Date appointed successfully. Confirmation email sent.")
        except DentalRecords.DoesNotExist:
            messages.error(request, "Dental record not found.")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "admin/dentalrequest.html", {"service_request": service_request})

# View dental schedules
def dental_schedule(request):
    if request.user.is_superuser or request.user.is_staff:
        schedules = DentalRecords.objects.filter(appointed=True)
        if request.method == "POST":
            student_id = request.POST.get("student_id")
            service_type = request.POST.get("service_type")
            
            # Retrieve the DentalRecord object
            dental_record = DentalRecords.objects.get(patient__student__student_id=student_id, service_type=service_type)
            
            # Create a TransactionRecord
            TransactionRecord.objects.create(
                patient=dental_record.patient,
                transac_type="Dental Service",
                transac_date=timezone.now()
            )
            
            # Delete the dental record
            dental_record.delete()
            
            messages.success(request, "Marked As Done")
            return render(request, "admin/dentalschedule.html", {"schedules": schedules})
        return render(request, "admin/dentalschedule.html", {"schedules": schedules})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

# List pwd
def pwd_list(request):
    if request.user.is_superuser or request.user.is_staff:
        pwd = MedicalClearance.objects.filter(riskassessment__pwd = True)
        if request.method == "POST":
            student_id = request.POST.get("student_id")
            if MedicalClearance.objects.filter(patient__student__student_id = student_id, riskassessment__pwd = True).exists():
                pwd_patient = MedicalClearance.objects.filter(patient__student__student_id = student_id, riskassessment__pwd = True)
                return render(request, "admin/pwdlist.html", {"pwds":pwd_patient})
            else:
                messages.error(request, "PWD Student not found")
                return render(request, "admin/pwdlist.html", {})
        return render(request, "admin/pwdlist.html", {"pwds":pwd})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

# View pwd in details
def pwd_detail(request, student_id):
    pwd = MedicalClearance.objects.get(patient__student__student_id = student_id)
    md = MedicalRequirement.objects.get(patient__student__student_id = student_id)
    return render(request, 'admin/pwddetails.html', {'pwd': pwd, "md": md})

# List all record of prescriptions
def view_prescription_records(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to access this page.")
    presc_record = PrescriptionRecord.objects.all()
    return render(request, "admin/prescriptionrecords.html", {"prescription_records": presc_record})

# List all record of emergency health assistance
def view_emergency_health_records(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to access this page.")
    emrgncy_record = EmergencyHealthAssistanceRecord.objects.all()
    return render(request, "admin/emergencyhealthrecords.html", {"emrgncy_record": emrgncy_record})

# Check if eligible for insurance
def check_insurance_availability(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")

        if EmergencyHealthAssistanceRecord.objects.filter(patient__student__student_id = student_id).exists():
            messages.success(request, "Done checking, you are eligible for an insurance")
            return render(request, "students/emergencyinsurance.html", {"eligible": True})
        else:
            messages.error(request, "Done checking, you are not eligible for an insurance")
            return render(request, "students/emergencyinsurance.html", {})
    return render(request, "students'/emergencyinsurance.html", {})

# Views for handling transactions
def transactions_view(request):
    transaction_type = request.GET.get('type', 'all')
    transaction_records = TransactionRecord.objects.all()

    if transaction_type != 'all':
        transaction_records = transaction_records.filter(transac_type=transaction_type)

    return render(request, 'admin/transactions.html', {'transaction_records': transaction_records})

def monthly_transactions_view(request):
    if request.method == 'POST':
        # Handle POST request
        selected_month = request.POST.get('selected_month')
        selected_year = request.POST.get('selected_year')
        transaction_type = request.POST.get('type', 'all')

        # Initialize the query set
        if selected_month and selected_year:
            # Convert selected month and year to integer
            selected_month = int(selected_month)
            selected_year = int(selected_year)

            # Filter transactions by the selected month and year
            transaction_records = TransactionRecord.objects.filter(
                transac_date__month=selected_month,
                transac_date__year=selected_year
            )
        else:
            transaction_records = TransactionRecord.objects.all()

        # Filter by transaction type if not 'all'
        if transaction_type != 'all':
            transaction_records = transaction_records.filter(transac_type=transaction_type)

        return render(request, 'admin/transactions.html', {
            'transaction_records': transaction_records,
            'filter_option': 'monthly',
            'selected_month': selected_month,
            'selected_year': selected_year,
            'transaction_type': transaction_type,
        })
    else:
        # Handle GET request
        print(request.GET)
        selected_month = request.GET.get('month')
        selected_year = request.GET.get('year')
        transaction_type = request.GET.get('type', 'all')
        print("This is a line break")
        print(selected_month)
        print(selected_year)
        print(transaction_type)
        # Initialize the query set
        if selected_month and selected_year:
            # Convert selected month and year to integer
            selected_month = int(selected_month)
            selected_year = int(selected_year)

            # Filter transactions by the selected month and year
            transaction_records = TransactionRecord.objects.filter(
                transac_date__month=selected_month,
                transac_date__year=selected_year
            )
        else:
            transaction_records = TransactionRecord.objects.all()

        # Filter by transaction type if not 'all'
        if transaction_type != 'all':
            transaction_records = transaction_records.filter(transac_type=transaction_type)

        month_name = calendar.month_name[selected_month]
        return render(request, 'admin/transactions.html', {
            'transaction_records': transaction_records,
            'filter_option': 'monthly',
            'selected_month': selected_month,
            'selected_year': selected_year,
            'transaction_type': transaction_type,
            'month_name': month_name,
            'monthly': True
        })


def daily_transactions_view(request):
    transaction_type = request.GET.get('type', 'all')
    transaction_records = TransactionRecord.objects.filter(transac_date__date=date.today())

    if transaction_type != 'all':
        transaction_records = transaction_records.filter(transac_type=transaction_type)
    today = date.today()
    month_name = calendar.month_name[today.month]

    return render(request, 'admin/transactions.html', {
        'transaction_records': transaction_records, 
        'transaction_type': transaction_type, 
        'month_name': month_name,
        'date_today': today.day,
        'year': today.year,
        'daily': True
    })

# def med_certificate_for_intrams(request, student_id):
#     if request.user.is_superuser or request.user.is_staff:
#         if request.method == "POST":
#             #student_request = StudentRequest.objects.get(student__student_id = student_id, request_type = "Medical Certificate for Intramurals")
#             #student_request.date_approved = datetime.now()
#             #student_request.save()
#             return render(request, "admin/med_cert.html", {"approve": True})
#         student = Student.objects.get(student_id=student_id)
#         messages.info(request, f"Issue Medical Certificate for {student.firstname.title()}")
#         return render(request, "admin/med_cert.html", {"student": student})
#     else:
#         return HttpResponseForbidden("You don't have permission to access this page.")

def med_cert(request, student_id):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to access this page.")
    patient = Patient.objects.get(student__student_id = student_id)

    if request.method == "POST":
        college = request.POST.get("college")
        year = request.POST.get("year")
        age = request.POST.get("age")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        bp = request.POST.get("bp")
        p = request.POST.get("p")
        t = request.POST.get("t")
        rr = request.POST.get("rr")
        sports_played = request.POST.get("sports_played")
        physically_able = request.POST.get("able") == "on"
        print(physically_able)
        physically_not_able = request.POST.get("not-able") == "on"

        if MedicalCertificate.objects.filter(patient__student__student_id = student_id).exists():
            med_cert = MedicalCertificate.objects.get(patient__student__student_id = student_id)
            med_cert.college = college
            med_cert.year = year
            med_cert.age = age
            med_cert.height = height
            med_cert.weight = weight
            med_cert.bp = bp
            med_cert.p = p
            med_cert.t = t
            med_cert.rr = rr
            med_cert.sports_played = sports_played
            med_cert.physically_able = physically_able
            med_cert.physically_not_able = physically_not_able
            med_cert.save()

            messages.success(request, "Record Updated")
            return render(request, "admin/med_cert.html", {"patient": patient, "cedicalcertificate": med_cert})
        
        med_cert = MedicalCertificate.objects.create(
            patient = patient,
            college = college,
            year = year,
            age = age,
            height = height,
            weight = weight,
            bp = bp,
            p = p,
            t = t,
            rr = rr,
            sports_played = sports_played,
            physically_able = physically_able,
            physically_not_able = physically_not_able
        )
        messages.success(request, "Medical certificate successfully created")
        return render(request, "admin/med_cert.html", {"patient": patient, "cedicalcertificate": med_cert})
    if MedicalCertificate.objects.filter(patient__student__student_id = student_id).exists():
        med_cert = MedicalCertificate.objects.get(patient__student__student_id = student_id)
        return render(request, "admin/med_cert.html", {"patient": patient, "cedicalcertificate": med_cert})
    messages.info(request, f"Issue Medical Certificate for {patient.student.firstname.title()}")
    return render(request, "admin/med_cert.html", {"patient": patient})

# For uploading student from a csv file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            print(reader)
            for row in reader:
                print(row)
                Student.objects.create(
                    student_id=row['\ufeffstudID'],
                    lrn=row['lrn'],
                    lastname=row['lname'],
                    firstname=row['fname'],
                    middlename=row['mi'],
                    degree=row['degree'],
                    year_level=row['year_level'],
                    sex=row['sex'],
                    email=row['email_add'],
                    contact_number=row['contactnum']
                )
            messages.success(request, 'File uploaded and data imported successfully')
        # return redirect('medical: upload')
        return render(request, 'upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
