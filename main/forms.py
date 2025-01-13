from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=100, required=True)
    lastname = forms.CharField(max_length=100, required=True)
    middlename = forms.CharField(max_length=100, required=False)
    degree = forms.CharField(max_length=100, required=True)
    year_level = forms.CharField(max_length=20, required=True)
    section = forms.ChoiceField(choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ], required=True)
    student_id = forms.CharField(max_length=20, required=True)
    sex = forms.CharField(max_length=1, required=True)
    lrn = forms.CharField(max_length=12, required=True)
    contact_number = forms.CharField(max_length=11, required=True)

    class Meta:
        model = User
        fields = (
            'email', 
            'password1', 
            'password2', 
            'firstname', 
            'lastname', 
            'middlename', 
            'degree',
            'year_level',
            'section',
            'student_id',
            'sex',
            'lrn',
            'contact_number'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email', '')

        if password1 and password2 and password1 == password2:
            if email and password1.lower() in email.lower():
                raise forms.ValidationError("Password cannot be too similar to your email address.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email