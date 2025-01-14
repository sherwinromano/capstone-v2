from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('recovery/', views.recovery, name='recovery'),
    path('password-reset/', views.password_reset, name='password-reset'),
    path('main/', views.main_view, name='main'),
    path('medical/', include('medical.urls', namespace='medical')),
    path('patient-form/', views.patient_form_view, name='patient_form'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('student-dashboard/', views.dashboard_view, name='student_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)