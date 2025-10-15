"""
medical_records/forms.py
Forms for Medical Records System
"""

from django import forms
from .models import MedicalRecord, Prescription, LabTest, VaccinationRecord, MedicalDocument


class MedicalRecordForm(forms.ModelForm):
    """Form for creating/editing medical records"""
    
    class Meta:
        model = MedicalRecord
        fields = [
            # Vital Signs
            'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'weight', 'height',
            # Medical Details
            'chief_complaint', 'present_illness', 'physical_examination',
            'diagnosis', 'treatment_plan', 'follow_up_instructions',
            # Additional
            'allergies', 'current_medications', 'past_medical_history',
            'family_history', 'social_history',
            # Follow-up
            'follow_up_required', 'follow_up_date',
        ]
        widgets = {
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 98.6',
                'step': '0.1'
            }),
            'blood_pressure_systolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Systolic (e.g., 120)'
            }),
            'blood_pressure_diastolic': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Diastolic (e.g., 80)'
            }),
            'heart_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 72'
            }),
            'respiratory_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 16'
            }),
            'oxygen_saturation': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 98'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg',
                'step': '0.1'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in cm',
                'step': '0.1'
            }),
            'chief_complaint': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Main reason for visit...'
            }),
            'present_illness': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'History of present illness...'
            }),
            'physical_examination': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Physical examination findings...'
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Medical diagnosis...'
            }),
            'treatment_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Recommended treatment...'
            }),
            'follow_up_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Follow-up instructions...'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Known allergies...'
            }),
            'current_medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Current medications...'
            }),
            'past_medical_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Past medical history...'
            }),
            'family_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Family medical history...'
            }),
            'social_history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Social history (smoking, alcohol, etc.)...'
            }),
            'follow_up_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'follow_up_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class PrescriptionForm(forms.ModelForm):
    """Form for adding prescriptions"""
    
    class Meta:
        model = Prescription
        fields = [
            'medication_name', 'dosage', 'frequency', 
            'duration', 'instructions', 'status', 'end_date'
        ]
        widgets = {
            'medication_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Amoxicillin'
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 500mg'
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Three times daily'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 7 days'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Special instructions (e.g., Take with food)...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class LabTestForm(forms.ModelForm):
    """Form for ordering lab tests"""
    
    class Meta:
        model = LabTest
        fields = [
            'test_name', 'test_type', 'description', 
            'instructions', 'status'
        ]
        widgets = {
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Complete Blood Count (CBC)'
            }),
            'test_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Test description...'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Pre-test instructions (e.g., Fasting required)...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class LabTestResultForm(forms.ModelForm):
    """Form for adding lab test results"""
    
    class Meta:
        model = LabTest
        fields = [
            'result', 'result_file', 'is_abnormal', 
            'requires_attention', 'notes', 'status'
        ]
        widgets = {
            'result': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Test results...'
            }),
            'result_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_abnormal': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'requires_attention': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class VaccinationRecordForm(forms.ModelForm):
    """Form for recording vaccinations"""
    
    class Meta:
        model = VaccinationRecord
        fields = [
            'vaccine_name', 'vaccine_type', 'manufacturer', 
            'batch_number', 'dose_number', 'administration_date',
            'administration_site', 'next_dose_date', 'side_effects', 'notes'
        ]
        widgets = {
            'vaccine_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., COVID-19 Vaccine'
            }),
            'vaccine_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., mRNA'
            }),
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Pfizer'
            }),
            'batch_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Batch number'
            }),
            'dose_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'administration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'administration_site': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Left arm'
            }),
            'next_dose_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'side_effects': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any side effects observed...'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...'
            }),
        }


class MedicalDocumentForm(forms.ModelForm):
    """Form for uploading medical documents"""
    
    class Meta:
        model = MedicalDocument
        fields = ['title', 'description', 'document_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Document description...'
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'
            }),
        }