from django import forms
from .models import Patient, MedicalHistory, RiskAssessment

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['student']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bloodtype': forms.Select(attrs={'class': 'form-select'}),
            'civil_status': forms.Select(attrs={'class': 'form-select'}),
            'parent_guardian_contact_number': forms.TextInput(attrs={
                'pattern': '09[0-9]{9}',
                'maxlength': '11',
                'placeholder': '09XXXXXXXXX'
            })
        }

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        exclude = ['patient']

class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        exclude = ['patient']
        widgets = {
            'disability_details': forms.Textarea(attrs={
                'rows': 3,
                'class': 'hidden',
                'data-depends-on': 'is_pwd'
            })
        }

# Add the missing UploadFileForm
class UploadFileForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    document_type = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
