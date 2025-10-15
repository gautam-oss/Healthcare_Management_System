"""
medical_records/admin.py
Admin Configuration for Medical Records System
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    MedicalRecord, Prescription, LabTest, 
    VaccinationRecord, MedicalDocument
)


class PrescriptionInline(admin.TabularInline):
    """Inline display of prescriptions in medical record"""
    model = Prescription
    extra = 0
    fields = ['medication_name', 'dosage', 'frequency', 'duration', 'status']
    readonly_fields = ['created_at']


class LabTestInline(admin.TabularInline):
    """Inline display of lab tests in medical record"""
    model = LabTest
    extra = 0
    fields = ['test_name', 'test_type', 'status', 'ordered_date']
    readonly_fields = ['ordered_date']


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    """Admin interface for Medical Records"""
    list_display = [
        'id', 'patient_name', 'doctor_name', 'appointment', 
        'diagnosis_preview', 'bmi_display', 'created_at'
    ]
    list_filter = ['created_at', 'follow_up_required', 'doctor__specialization']
    search_fields = [
        'patient__user__first_name', 'patient__user__last_name',
        'doctor__user__first_name', 'doctor__user__last_name',
        'diagnosis', 'chief_complaint'
    ]
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'bmi_display', 'blood_pressure_display']
    inlines = [PrescriptionInline, LabTestInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('appointment', 'patient', 'doctor', 'created_at', 'updated_at')
        }),
        ('Vital Signs', {
            'fields': (
                'temperature', 
                ('blood_pressure_systolic', 'blood_pressure_diastolic', 'blood_pressure_display'),
                'heart_rate', 'respiratory_rate', 'oxygen_saturation',
                ('weight', 'height', 'bmi_display')
            ),
            'classes': ('collapse',)
        }),
        ('Medical Information', {
            'fields': (
                'chief_complaint', 'present_illness', 'physical_examination',
                'diagnosis', 'treatment_plan', 'follow_up_instructions'
            )
        }),
        ('Patient History', {
            'fields': (
                'allergies', 'current_medications', 'past_medical_history',
                'family_history', 'social_history'
            ),
            'classes': ('collapse',)
        }),
        ('Follow-up', {
            'fields': ('follow_up_required', 'follow_up_date')
        }),
    )
    
    def patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.username
    patient_name.short_description = 'Patient'
    patient_name.admin_order_field = 'patient__user__last_name'
    
    def doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name() or obj.doctor.user.username}"
    doctor_name.short_description = 'Doctor'
    doctor_name.admin_order_field = 'doctor__user__last_name'
    
    def diagnosis_preview(self, obj):
        return obj.diagnosis[:50] + '...' if len(obj.diagnosis) > 50 else obj.diagnosis
    diagnosis_preview.short_description = 'Diagnosis'
    
    def bmi_display(self, obj):
        bmi = obj.bmi
        if bmi:
            if bmi < 18.5:
                color = 'blue'
                status = 'Underweight'
            elif bmi < 25:
                color = 'green'
                status = 'Normal'
            elif bmi < 30:
                color = 'orange'
                status = 'Overweight'
            else:
                color = 'red'
                status = 'Obese'
            return format_html(
                '<span style="color: {};">{} ({})</span>',
                color, bmi, status
            )
        return '-'
    bmi_display.short_description = 'BMI'
    
    def blood_pressure_display(self, obj):
        bp = obj.blood_pressure
        if bp:
            systolic = obj.blood_pressure_systolic
            if systolic < 120:
                color = 'green'
            elif systolic < 140:
                color = 'orange'
            else:
                color = 'red'
            return format_html('<span style="color: {};">{}</span>', color, bp)
        return '-'
    blood_pressure_display.short_description = 'Blood Pressure'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    """Admin interface for Prescriptions"""
    list_display = [
        'id', 'patient_name', 'medication_name', 'dosage', 
        'frequency', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'doctor__specialization']
    search_fields = [
        'medication_name', 'patient__user__first_name', 
        'patient__user__last_name', 'doctor__user__first_name'
    ]
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Prescription Details', {
            'fields': ('medical_record', 'patient', 'doctor')
        }),
        ('Medication Information', {
            'fields': ('medication_name', 'dosage', 'frequency', 'duration', 'instructions')
        }),
        ('Status', {
            'fields': ('status', 'start_date', 'end_date', 'created_at', 'updated_at')
        }),
    )
    
    def patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.username
    patient_name.short_description = 'Patient'
    
    def status_badge(self, obj):
        colors = {
            'active': 'green',
            'completed': 'blue',
            'discontinued': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    """Admin interface for Lab Tests"""
    list_display = [
        'id', 'patient_name', 'test_name', 'test_type', 
        'status_badge', 'abnormal_flag', 'ordered_date'
    ]
    list_filter = ['status', 'test_type', 'is_abnormal', 'requires_attention', 'ordered_date']
    search_fields = [
        'test_name', 'patient__user__first_name', 
        'patient__user__last_name', 'doctor__user__first_name'
    ]
    date_hierarchy = 'ordered_date'
    readonly_fields = ['ordered_date', 'updated_at']
    
    fieldsets = (
        ('Test Information', {
            'fields': ('medical_record', 'patient', 'doctor', 'test_name', 'test_type')
        }),
        ('Details', {
            'fields': ('description', 'instructions', 'status')
        }),
        ('Results', {
            'fields': ('result', 'result_file', 'result_date', 'is_abnormal', 'requires_attention', 'notes')
        }),
        ('Timestamps', {
            'fields': ('ordered_date', 'updated_at')
        }),
    )
    
    def patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.username
    patient_name.short_description = 'Patient'
    
    def status_badge(self, obj):
        colors = {
            'ordered': 'blue',
            'in_progress': 'orange',
            'completed': 'green',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def abnormal_flag(self, obj):
        if obj.is_abnormal:
            return format_html('<span style="color: red; font-weight: bold;">⚠ ABNORMAL</span>')
        return '-'
    abnormal_flag.short_description = 'Flag'


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    """Admin interface for Vaccination Records"""
    list_display = [
        'id', 'patient_name', 'vaccine_name', 'dose_number', 
        'administration_date', 'next_dose_date'
    ]
    list_filter = ['administration_date', 'vaccine_name', 'dose_number']
    search_fields = [
        'vaccine_name', 'patient__user__first_name', 
        'patient__user__last_name', 'batch_number'
    ]
    date_hierarchy = 'administration_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Patient & Provider', {
            'fields': ('patient', 'administered_by')
        }),
        ('Vaccine Information', {
            'fields': ('vaccine_name', 'vaccine_type', 'manufacturer', 'batch_number')
        }),
        ('Administration Details', {
            'fields': ('dose_number', 'administration_date', 'administration_site', 'next_dose_date')
        }),
        ('Additional Information', {
            'fields': ('side_effects', 'notes', 'created_at', 'updated_at')
        }),
    )
    
    def patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.username
    patient_name.short_description = 'Patient'


@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    """Admin interface for Medical Documents"""
    list_display = [
        'id', 'title', 'patient_name', 'document_type', 
        'file_size_display', 'uploaded_at'
    ]
    list_filter = ['document_type', 'uploaded_at']
    search_fields = [
        'title', 'description', 'patient__user__first_name', 
        'patient__user__last_name'
    ]
    date_hierarchy = 'uploaded_at'
    readonly_fields = ['file_size', 'uploaded_at']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'description', 'document_type')
        }),
        ('File & Patient', {
            'fields': ('file', 'file_size', 'patient', 'medical_record', 'uploaded_by')
        }),
        ('Timestamp', {
            'fields': ('uploaded_at',)
        }),
    )
    
    def patient_name(self, obj):
        return obj.patient.user.get_full_name() or obj.patient.user.username
    patient_name.short_description = 'Patient'
    
    def file_size_display(self, obj):
        if obj.file_size:
            size_mb = obj.file_size / (1024 * 1024)
            if size_mb < 1:
                return f"{obj.file_size / 1024:.2f} KB"
            return f"{size_mb:.2f} MB"
        return '-'
    file_size_display.short_description = 'File Size'