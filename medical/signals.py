from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Student as MainStudent
from medical.models import Student as MedicalStudent

@receiver(post_save, sender=MainStudent)
def create_medical_student(sender, instance, created, **kwargs):
    if created:
        MedicalStudent.objects.create(
            student_id=instance.student_id,
            lrn=instance.lrn,
            lastname=instance.lastname,
            firstname=instance.firstname,
            middlename=instance.middlename,
            degree=instance.degree,
            year_level=instance.year_level,
            sex=instance.sex,
            email=instance.email,
            contact_number=instance.contact_number
        )
