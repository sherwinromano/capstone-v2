from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'lrn', 'lastname', 'firstname', 'degree', 'year_level')
    list_filter = ('degree', 'year_level', 'sex')
    search_fields = ('student_id', 'lrn', 'lastname', 'firstname', 'email')
    ordering = ('lastname', 'firstname')
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'student_id', 
                'lrn',
                ('lastname', 'firstname', 'middlename'),
                'sex',
            )
        }),
        ('Academic Information', {
            'fields': (
                'degree',
                'year_level',
            )
        }),
        ('Contact Information', {
            'fields': (
                'email',
                'contact_number',
            )
        }),
    )
