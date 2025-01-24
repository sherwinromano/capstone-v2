from django.db import models
import os
from django.contrib.auth.models import User
from main.models import Student

# Create your models here.
class Student(models.Model):
    student_id = models.CharField(max_length=100, primary_key=True)
    lrn = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100)
    year_level = models.PositiveIntegerField()
    sex = models.CharField(max_length=6)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.lastname}, {self.firstname}"

class Patient(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    birth_date = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    bloodtype = models.CharField(max_length=20)
    allergies = models.CharField(max_length=100)
    medications = models.CharField(max_length=100)
    home_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    civil_status = models.CharField(max_length=20)
    number_of_children = models.PositiveIntegerField(null=True, blank=True)
    academic_year = models.CharField(max_length=20)
    section = models.CharField(max_length=20)
    parent_guardian = models.CharField(max_length=100)
    parent_guardian_contact_number = models.CharField(max_length=15, null=True, blank=True)
    examination = models.OneToOneField('PhysicalExamination', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.firstname} {self.student.lastname}"

class PhysicalExamination(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_of_physical_examination = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Physical Exam - {self.student.firstname} {self.student.lastname}"

class MedicalHistory(models.Model):
    examination = models.OneToOneField(PhysicalExamination, on_delete=models.CASCADE)
    tuberculosis = models.BooleanField(default=False)
    hypertension = models.BooleanField(default=False)
    heart_disease = models.BooleanField(default=False)
    hernia = models.BooleanField(default=False)
    epilepsy = models.BooleanField(default=False)
    peptic_ulcer = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    insomnia = models.BooleanField(default=False)
    malaria = models.BooleanField(default=False)
    venereal_disease = models.BooleanField(default=False)
    allergic_reaction = models.BooleanField(default=False)
    nervous_breakdown = models.BooleanField(default=False)
    jaundice = models.BooleanField(default=False)
    others = models.CharField(max_length=100, null=True, blank=True)
    no_history = models.BooleanField(default=False)
    hospital_admission = models.CharField(max_length=255, null=True, blank=True)
    medications = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Medical history of {self.examination.student.firstname} {self.examination.student.lastname}"

class FamilyMedicalHistory(models.Model):
    examination = models.OneToOneField(PhysicalExamination, on_delete=models.CASCADE)
    hypertension = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    cancer = models.BooleanField(default=True)
    tuberculosis = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    bleeding_disorder = models.BooleanField(default=False)
    epilepsy = models.BooleanField(default=False)
    mental_disorder = models.BooleanField(default=False)
    no_history = models.BooleanField(default=False)
    other_medical_history = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Family Medical History of {self.examination.student.firstname} {self.examination.student.lastname}"

class ObgyneHistory(models.Model):
    examination = models.OneToOneField(PhysicalExamination, on_delete=models.CASCADE)
    menarche = models.CharField(max_length=100, null=True, blank=True)
    lmp = models.CharField(max_length=100, null=True, blank=True)
    pap_smear = models.CharField(max_length=100, null=True, blank=True)
    gravida = models.CharField(max_length=10, null=True, blank=True)
    para = models.CharField(max_length=10, null=True, blank=True)
    menopause = models.CharField(max_length=100, null=True, blank=True)
    additional_history = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"OB-GYNE History of {self.examination.student.firstname} {self.examination.student.lastname}"
    
class MedicalClearance(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Medical clearance for {self.patient.student.firstname} {self.patient.student.lastname}"

class RiskAssessment(models.Model):
    id = models.AutoField(primary_key=True)
    clearance = models.OneToOneField(MedicalClearance, on_delete=models.CASCADE)
    cardiovascular_disease = models.BooleanField(default=False)
    chronic_lung_disease = models.BooleanField(default=False)
    chronic_renal_disease = models.BooleanField(default=False)
    chronic_liver_disease = models.BooleanField(default=False)
    cancer = models.BooleanField(default=False)
    autoimmune_disease = models.BooleanField(default=False)
    pwd = models.BooleanField(default=False)
    disability = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Risk Assessment for {self.clearance}"

    class Meta:
        verbose_name = "Risk Assessment"
        verbose_name_plural = "Risk Assessments"
    
    # def pwd_path(instance, filename, field_name):
    #     return os.path.join('pwd', f'{instance.clearance.student.lastname}_{instance.clearance.student.firstname}', field_name, filename)
    
    # def pwd_idcard(instance, filename):
    #     return RiskAssessment.pwd_path(instance, filename, 'pwd_card')
    
    # pwd_id_card = models.FileField(upload_to=pwd_path, null=True, blank=True)
    
class MedicalRequirement(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    #clearance = models.OneToOneField(MedicalClearance, on_delete=models.CASCADE)
    vaccination_type = models.CharField(max_length=50, null=True, blank=True)
    vaccinated_1st = models.BooleanField(default=False, null=True, blank=True)
    vaccinated_2nd = models.BooleanField(default=False, null=True, blank=True)
    vaccinated_booster = models.BooleanField(default=False, null=True, blank=True)

    x_ray_remarks = models.CharField(max_length=100, null=True, blank=True)
    cbc_remarks = models.CharField(max_length=100, null=True, blank=True)
    drug_test_remarks = models.CharField(max_length=100, null=True, blank=True)
    stool_examination_remarks = models.CharField(max_length=100, null=True, blank=True)

    def patient_directory_path(instance, filename, field_name):
        return os.path.join('medical', f'{instance.patient.student.lastname}_{instance.patient.student.firstname}', field_name, filename)
    
    def chest_xray_path(instance, filename):
        return MedicalRequirement.patient_directory_path(instance, filename, 'chest_xrays')
    
    def cbc_path(instance, filename):
        return MedicalRequirement.patient_directory_path(instance, filename, 'cbc')
    
    def drug_test_path(instance, filename):
        return MedicalRequirement.patient_directory_path(instance, filename, 'drug_tests')
    
    def stool_examination_path(instance, filename):
        return MedicalRequirement.patient_directory_path(instance, filename, 'stool_exam')
    
    def pwd_id_card_path(instance, filename):
        return MedicalRequirement.patient_directory_path(instance, filename, 'pwd_card')

    chest_xray = models.FileField(upload_to=chest_xray_path)
    cbc = models.FileField(upload_to=cbc_path)
    drug_test = models.FileField(upload_to=drug_test_path)
    stool_examination = models.FileField(upload_to=stool_examination_path)
    pwd_card = models.FileField(upload_to=pwd_id_card_path, null=True, blank=True)

    def __str__(self):
        return f"Medical Requirements for {self.patient.student.firstname} {self.patient.student.lastname}"

    # def delete(self, *args, **kwargs):
    #     self.chest_xray.delete(save=False)
    #     self.cbc.delete(save=False)
    #     self.drug_test.delete(save=False)
    #     self.stool_examination.delete(save=False)
    #     super().delete(*args, **kwargs)

class EligibilityForm(models.Model):
    patient = models.OneToOneField(Patient, primary_key=True, on_delete=models.CASCADE)
    # age = models.PositiveIntegerField()
    # birth_date = models.CharField(max_length=100)
    # weight = models.FloatField()
    # height = models.FloatField()
    # blood_type = models.CharField(max_length=20)
    # allergies = models.CharField(max_length=100)
    # medications = models.CharField(max_length=100)
    #address = models.CharField(max_length=50)
    blood_pressure = models.CharField(max_length=20)
    competetions = models.CharField(max_length=100)
    date_of_event = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    date_of_examination = models.CharField(max_length=100)
    liscence_number = models.CharField(max_length=50)
    validity_date = models.CharField(max_length=100)
    
class MedicalCertificate(models.Model):
    patient = models.OneToOneField(Patient, primary_key=True, on_delete=models.CASCADE)
    college = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    bp = models.CharField(max_length=20)
    p = models.CharField(max_length=20)
    t = models.CharField(max_length=20)
    rr = models.CharField(max_length=20)
    sports_played = models.CharField(max_length=255)
    physically_able = models.BooleanField(default=False)
    physically_not_able = models.BooleanField(default=False)

class PatientRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100)
    approve = models.BooleanField(default=False)
    date_requested = models.DateTimeField()
    date_approved = models.DateTimeField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.request_type} request for {self.patient.student.firstname})"
    
class PrescriptionRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    problem = models.CharField(max_length=50)
    treatment = models.CharField(max_length=50)
    date_prescribed = models.CharField(max_length=100)

    def __str__(self):
        return f"Prescription for {self.patient.student.firstname} {self.patient.student.lastname}"

class DentalRecords(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50)
    date_requested = models.DateTimeField()
    date_appointed = models.DateField(null=True)
    appointed = models.BooleanField(default=False)
    # def __str__(self):
    #     pass

class EmergencyHealthAssistanceRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)
    date_assisted = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.patient.student.firstname} {self.patient.student.lastname}"

class TransactionRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    transac_type = models.CharField(max_length=100)
    transac_date = models.DateTimeField()

    # def __str__(self):
    #     return f"{self.student.firstname} {self.student.lastname}"
    
class MentalHealthRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescription = models.FileField(upload_to='mental_health/prescriptions/')
    certification = models.FileField(upload_to='mental_health/certifications/')
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Mental Health Record - {self.patient.student.student_id}"
    