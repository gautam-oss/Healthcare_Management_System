"""
medical_records/models.py
Complete Medical Records System with Prescriptions, Test Results, and Medical History
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User, Patient, Doctor
from appointments.models import Appointment


class MedicalRecord(models.Model):
    """Main medical record for each appointment"""
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='medical_record'
    )
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='medical_records'
    )
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='created_records'
    )
    
    # Vital Signs
    temperature = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        null=True, 
        blank=True,
        help_text="Temperature in °F"
    )
    blood_pressure_systolic = models.IntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(250)],
        null=True, 
        blank=True
    )
    blood_pressure_diastolic = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(150)],
        null=True, 
        blank=True
    )
    heart_rate = models.IntegerField(
        validators=[MinValueValidator(40), MaxValueValidator(200)],
        null=True, 
        blank=True,
        help_text="Beats per minute"
    )
    respiratory_rate = models.IntegerField(
        validators=[MinValueValidator(8), MaxValueValidator(40)],
        null=True, 
        blank=True,
        help_text="Breaths per minute"
    )
    oxygen_saturation = models.IntegerField(
        validators=[MinValueValidator(70), MaxValueValidator(100)],
        null=True, 
        blank=True,
        help_text="SpO2 percentage"
    )
    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Weight in kg"
    )
    height = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Height in cm"
    )
    
    # Medical Details
    chief_complaint = models.TextField(help_text="Main reason for visit")
    present_illness = models.TextField(blank=True, help_text="History of present illness")
    physical_examination = models.TextField(blank=True)
    diagnosis = models.TextField(help_text="Medical diagnosis")
    treatment_plan = models.TextField(help_text="Recommended treatment")
    follow_up_instructions = models.TextField(blank=True)
    
    # Additional Notes
    allergies = models.TextField(blank=True, help_text="Known allergies")
    current_medications = models.TextField(blank=True)
    past_medical_history = models.TextField(blank=True)
    family_history = models.TextField(blank=True)
    social_history = models.TextField(blank=True)
    
    # Follow-up
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_required = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['doctor', '-created_at']),
        ]
    
    def __str__(self):
        return f"Medical Record - {self.patient.user.get_full_name()} - {self.created_at.date()}"
    
    @property
    def bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.weight and self.height:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 2)
        return None
    
    @property
    def blood_pressure(self):
        """Return formatted blood pressure"""
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
        return None


class Prescription(models.Model):
    """Prescription for medications"""
    medical_record = models.ForeignKey(
        MedicalRecord, 
        on_delete=models.CASCADE, 
        related_name='prescriptions'
    )
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='prescriptions'
    )
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='prescribed_medications'
    )
    
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg")
    frequency = models.CharField(max_length=100, help_text="e.g., Twice daily")
    duration = models.CharField(max_length=100, help_text="e.g., 7 days")
    instructions = models.TextField(blank=True, help_text="Special instructions")
    
    # Status tracking
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('discontinued', 'Discontinued'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.medication_name} - {self.patient.user.get_full_name()}"


class LabTest(models.Model):
    """Laboratory test orders and results"""
    medical_record = models.ForeignKey(
        MedicalRecord, 
        on_delete=models.CASCADE, 
        related_name='lab_tests'
    )
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='lab_tests'
    )
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='ordered_tests'
    )
    
    test_name = models.CharField(max_length=200)
    test_type = models.CharField(
        max_length=100,
        choices=[
            ('blood', 'Blood Test'),
            ('urine', 'Urine Test'),
            ('imaging', 'Imaging'),
            ('biopsy', 'Biopsy'),
            ('other', 'Other'),
        ],
        default='blood'
    )
    
    # Test details
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True, help_text="Pre-test instructions")
    
    # Status
    STATUS_CHOICES = [
        ('ordered', 'Ordered'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    
    # Results
    result = models.TextField(blank=True)
    result_file = models.FileField(upload_to='lab_results/', null=True, blank=True)
    result_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Flags for abnormal results
    is_abnormal = models.BooleanField(default=False)
    requires_attention = models.BooleanField(default=False)
    
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ordered_date']
    
    def __str__(self):
        return f"{self.test_name} - {self.patient.user.get_full_name()} - {self.status}"


class VaccinationRecord(models.Model):
    """Track patient vaccinations"""
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='vaccinations'
    )
    administered_by = models.ForeignKey(
        Doctor, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='administered_vaccines'
    )
    
    vaccine_name = models.CharField(max_length=200)
    vaccine_type = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=100, blank=True)
    
    dose_number = models.IntegerField(default=1, help_text="Which dose (1st, 2nd, booster)")
    administration_date = models.DateField()
    administration_site = models.CharField(
        max_length=100, 
        blank=True,
        help_text="e.g., Left arm, Right arm"
    )
    
    next_dose_date = models.DateField(null=True, blank=True)
    
    # Side effects
    side_effects = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-administration_date']
    
    def __str__(self):
        return f"{self.vaccine_name} - {self.patient.user.get_full_name()} - Dose {self.dose_number}"


class MedicalDocument(models.Model):
    """Store medical documents and reports"""
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='medical_documents'
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='uploaded_documents'
    )
    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('lab_report', 'Lab Report'),
            ('imaging', 'Imaging'),
            ('prescription', 'Prescription'),
            ('discharge_summary', 'Discharge Summary'),
            ('insurance', 'Insurance Document'),
            ('other', 'Other'),
        ],
        default='other'
    )
    
    file = models.FileField(upload_to='medical_documents/')
    file_size = models.IntegerField(help_text="File size in bytes", null=True, blank=True)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.patient.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)