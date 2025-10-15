"""
medical_records/urls.py - UPDATED VERSION
Replace your existing medical_records/urls.py with this
"""

from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    # Dashboard & Timeline
    path('dashboard/', views.medical_dashboard, name='dashboard'),
    path('timeline/', views.patient_health_timeline, name='timeline'),
    
    # Medical Records (General)
    path('', views.medical_records_list, name='list'),
    path('<int:record_id>/', views.medical_record_detail, name='detail'),
    path('create/<int:appointment_id>/', views.create_medical_record, name='create'),
    path('edit/<int:record_id>/', views.edit_medical_record, name='edit'),
    
    # NEW: Simple Doctor's Patient List
    path('doctor/my-patients/', views.doctor_my_patients, name='doctor_my_patients'),
    
    # Prescriptions
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('<int:record_id>/add-prescription/', views.add_prescription, name='add_prescription'),
    
    # Lab Tests
    path('lab-tests/', views.lab_test_list, name='lab_test_list'),
    path('<int:record_id>/order-lab-test/', views.order_lab_test, name='order_lab_test'),
    path('lab-test/<int:test_id>/add-result/', views.add_lab_result, name='add_lab_result'),
    
    # Vaccinations
    path('vaccinations/', views.vaccination_list, name='vaccination_list'),
    path('vaccinations/add/', views.add_vaccination, name='add_vaccination'),
    path('vaccinations/add/<int:patient_id>/', views.add_vaccination, name='add_vaccination_for_patient'),
    
    # Documents
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('<int:record_id>/upload-document/', views.upload_document, name='upload_document_for_record'),
]