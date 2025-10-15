"""
medical_records/views.py
Views for Medical Records System - COMPLETE UPDATED VERSION
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.utils import timezone
from django.core.paginator import Paginator

from .models import (
    MedicalRecord, Prescription, LabTest, 
    VaccinationRecord, MedicalDocument
)
from .forms import (
    MedicalRecordForm, PrescriptionForm, LabTestForm, 
    LabTestResultForm, VaccinationRecordForm, MedicalDocumentForm
)
from appointments.models import Appointment
from users.models import Patient, Doctor


@login_required
def medical_records_list(request):
    """List all medical records (filtered by user type)"""
    if hasattr(request.user, 'patient'):
        records = MedicalRecord.objects.filter(
            patient=request.user.patient
        ).select_related('doctor__user', 'appointment')
    elif hasattr(request.user, 'doctor'):
        records = MedicalRecord.objects.filter(
            doctor=request.user.doctor
        ).select_related('patient__user', 'appointment')
    else:
        records = MedicalRecord.objects.none()
    
    context = {
        'records': records,
        'total_records': records.count(),
    }
    return render(request, 'medical_records/list.html', context)


@login_required
def medical_record_detail(request, record_id):
    """View detailed medical record"""
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    if hasattr(request.user, 'patient'):
        if record.patient != request.user.patient:
            return HttpResponseForbidden("You don't have permission to view this record.")
    elif hasattr(request.user, 'doctor'):
        if record.doctor != request.user.doctor:
            return HttpResponseForbidden("You don't have permission to view this record.")
    else:
        return HttpResponseForbidden("Access denied.")
    
    prescriptions = record.prescriptions.all()
    lab_tests = record.lab_tests.all()
    documents = record.documents.all()
    
    context = {
        'record': record,
        'prescriptions': prescriptions,
        'lab_tests': lab_tests,
        'documents': documents,
    }
    return render(request, 'medical_records/detail.html', context)


@login_required
def create_medical_record(request, appointment_id):
    """Create medical record for an appointment (Doctor only)"""
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can create medical records.')
        return redirect('users:dashboard')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if appointment.doctor != request.user.doctor:
        return HttpResponseForbidden("You don't have permission to create records for this appointment.")
    
    if hasattr(appointment, 'medical_record'):
        messages.info(request, 'Medical record already exists for this appointment.')
        return redirect('medical_records:detail', record_id=appointment.medical_record.id)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.appointment = appointment
            record.patient = appointment.patient
            record.doctor = request.user.doctor
            record.save()
            
            appointment.status = 'completed'
            appointment.save()
            
            messages.success(request, 'Medical record created successfully!')
            return redirect('medical_records:detail', record_id=record.id)
    else:
        form = MedicalRecordForm()
    
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'medical_records/create.html', context)


@login_required
def edit_medical_record(request, record_id):
    """Edit medical record (Doctor only)"""
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can edit medical records.')
        return redirect('users:dashboard')
    
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    if record.doctor != request.user.doctor:
        return HttpResponseForbidden("You don't have permission to edit this record.")
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical record updated successfully!')
            return redirect('medical_records:detail', record_id=record.id)
    else:
        form = MedicalRecordForm(instance=record)
    
    context = {
        'form': form,
        'record': record,
    }
    return render(request, 'medical_records/edit.html', context)


@login_required
def add_prescription(request, record_id):
    """Add prescription to medical record (Doctor only)"""
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can add prescriptions.')
        return redirect('users:dashboard')
    
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    if record.doctor != request.user.doctor:
        return HttpResponseForbidden("Permission denied.")
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.medical_record = record
            prescription.patient = record.patient
            prescription.doctor = request.user.doctor
            prescription.save()
            
            messages.success(request, 'Prescription added successfully!')
            return redirect('medical_records:detail', record_id=record.id)
    else:
        form = PrescriptionForm()
    
    context = {
        'form': form,
        'record': record,
    }
    return render(request, 'medical_records/add_prescription.html', context)


@login_required
def prescription_list(request):
    """List all prescriptions for current user"""
    if hasattr(request.user, 'patient'):
        prescriptions = Prescription.objects.filter(
            patient=request.user.patient
        ).select_related('doctor__user', 'medical_record').order_by('-created_at')
    elif hasattr(request.user, 'doctor'):
        prescriptions = Prescription.objects.filter(
            doctor=request.user.doctor
        ).select_related('patient__user', 'medical_record').order_by('-created_at')
    else:
        prescriptions = Prescription.objects.none()
    
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        prescriptions = prescriptions.filter(status=status_filter)
    
    context = {
        'prescriptions': prescriptions,
        'status_filter': status_filter,
        'active_count': prescriptions.filter(status='active').count(),
        'completed_count': prescriptions.filter(status='completed').count(),
    }
    return render(request, 'medical_records/prescription_list.html', context)


@login_required
def order_lab_test(request, record_id):
    """Order lab test (Doctor only)"""
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can order lab tests.')
        return redirect('users:dashboard')
    
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    if record.doctor != request.user.doctor:
        return HttpResponseForbidden("Permission denied.")
    
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            lab_test = form.save(commit=False)
            lab_test.medical_record = record
            lab_test.patient = record.patient
            lab_test.doctor = request.user.doctor
            lab_test.save()
            
            messages.success(request, 'Lab test ordered successfully!')
            return redirect('medical_records:detail', record_id=record.id)
    else:
        form = LabTestForm()
    
    context = {
        'form': form,
        'record': record,
    }
    return render(request, 'medical_records/order_lab_test.html', context)


@login_required
def lab_test_list(request):
    """List all lab tests for current user"""
    if hasattr(request.user, 'patient'):
        lab_tests = LabTest.objects.filter(
            patient=request.user.patient
        ).select_related('doctor__user', 'medical_record').order_by('-ordered_date')
    elif hasattr(request.user, 'doctor'):
        lab_tests = LabTest.objects.filter(
            doctor=request.user.doctor
        ).select_related('patient__user', 'medical_record').order_by('-ordered_date')
    else:
        lab_tests = LabTest.objects.none()
    
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        lab_tests = lab_tests.filter(status=status_filter)
    
    context = {
        'lab_tests': lab_tests,
        'status_filter': status_filter,
        'pending_count': lab_tests.filter(status__in=['ordered', 'in_progress']).count(),
        'completed_count': lab_tests.filter(status='completed').count(),
    }
    return render(request, 'medical_records/lab_test_list.html', context)


@login_required
def add_lab_result(request, test_id):
    """Add lab test result (Doctor/Lab Staff only)"""
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only authorized personnel can add lab results.')
        return redirect('users:dashboard')
    
    lab_test = get_object_or_404(LabTest, id=test_id)
    
    if request.method == 'POST':
        form = LabTestResultForm(request.POST, request.FILES, instance=lab_test)
        if form.is_valid():
            result = form.save(commit=False)
            result.result_date = timezone.now()
            result.save()
            
            messages.success(request, 'Lab result added successfully!')
            return redirect('medical_records:lab_test_list')
    else:
        form = LabTestResultForm(instance=lab_test)
    
    context = {
        'form': form,
        'lab_test': lab_test,
    }
    return render(request, 'medical_records/add_lab_result.html', context)


@login_required
def vaccination_list(request):
    """List all vaccinations"""
    if hasattr(request.user, 'patient'):
        vaccinations = VaccinationRecord.objects.filter(
            patient=request.user.patient
        ).select_related('administered_by__user').order_by('-administration_date')
    elif hasattr(request.user, 'doctor'):
        vaccinations = VaccinationRecord.objects.filter(
            administered_by=request.user.doctor
        ).select_related('patient__user').order_by('-administration_date')
    else:
        vaccinations = VaccinationRecord.objects.none()
    
    context = {
        'vaccinations': vaccinations,
    }
    return render(request, 'medical_records/vaccination_list.html', context)


@login_required
def add_vaccination(request, patient_id=None):
    """Add vaccination record (Doctor only)"""
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can add vaccination records.')
        return redirect('users:dashboard')
    
    patient = None
    if patient_id:
        patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            if patient:
                vaccination.patient = patient
            vaccination.administered_by = request.user.doctor
            vaccination.save()
            
            messages.success(request, 'Vaccination record added successfully!')
            return redirect('medical_records:vaccination_list')
    else:
        form = VaccinationRecordForm()
    
    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'medical_records/add_vaccination.html', context)


@login_required
def document_list(request):
    """List all medical documents"""
    if hasattr(request.user, 'patient'):
        documents = MedicalDocument.objects.filter(
            patient=request.user.patient
        ).select_related('uploaded_by').order_by('-uploaded_at')
    elif hasattr(request.user, 'doctor'):
        documents = MedicalDocument.objects.filter(
            patient__in=Patient.objects.filter(
                medical_records__doctor=request.user.doctor
            )
        ).distinct().select_related('patient__user', 'uploaded_by').order_by('-uploaded_at')
    else:
        documents = MedicalDocument.objects.none()
    
    context = {
        'documents': documents,
    }
    return render(request, 'medical_records/document_list.html', context)


@login_required
def upload_document(request, record_id=None):
    """Upload medical document"""
    record = None
    patient = None
    
    if record_id:
        record = get_object_or_404(MedicalRecord, id=record_id)
        patient = record.patient
        
        if hasattr(request.user, 'patient'):
            if record.patient != request.user.patient:
                return HttpResponseForbidden("Permission denied.")
        elif hasattr(request.user, 'doctor'):
            if record.doctor != request.user.doctor:
                return HttpResponseForbidden("Permission denied.")
    elif hasattr(request.user, 'patient'):
        patient = request.user.patient
    
    if request.method == 'POST':
        form = MedicalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.patient = patient
            document.uploaded_by = request.user
            if record:
                document.medical_record = record
            document.save()
            
            messages.success(request, 'Document uploaded successfully!')
            return redirect('medical_records:document_list')
    else:
        form = MedicalDocumentForm()
    
    context = {
        'form': form,
        'record': record,
    }
    return render(request, 'medical_records/upload_document.html', context)


@login_required
def medical_dashboard(request):
    """Medical records dashboard with statistics"""
    context = {}
    
    if hasattr(request.user, 'patient'):
        patient = request.user.patient
        
        context.update({
            'total_records': MedicalRecord.objects.filter(patient=patient).count(),
            'active_prescriptions': Prescription.objects.filter(
                patient=patient, status='active'
            ).count(),
            'pending_tests': LabTest.objects.filter(
                patient=patient, status__in=['ordered', 'in_progress']
            ).count(),
            'total_vaccinations': VaccinationRecord.objects.filter(patient=patient).count(),
            'recent_records': MedicalRecord.objects.filter(patient=patient)[:5],
            'active_prescriptions_list': Prescription.objects.filter(
                patient=patient, status='active'
            )[:5],
            'upcoming_vaccinations': VaccinationRecord.objects.filter(
                patient=patient, 
                next_dose_date__gte=timezone.now().date()
            ).order_by('next_dose_date')[:5],
        })
        
    elif hasattr(request.user, 'doctor'):
        doctor = request.user.doctor
        
        context.update({
            'total_records': MedicalRecord.objects.filter(doctor=doctor).count(),
            'total_prescriptions': Prescription.objects.filter(doctor=doctor).count(),
            'pending_tests': LabTest.objects.filter(
                doctor=doctor, status__in=['ordered', 'in_progress']
            ).count(),
            'total_vaccinations': VaccinationRecord.objects.filter(
                administered_by=doctor
            ).count(),
            'recent_records': MedicalRecord.objects.filter(doctor=doctor)[:5],
            'pending_tests_list': LabTest.objects.filter(
                doctor=doctor, status__in=['ordered', 'in_progress']
            )[:5],
        })
    
    return render(request, 'medical_records/dashboard.html', context)


@login_required
def patient_health_timeline(request):
    """Complete health timeline for patient"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Only patients can view their health timeline.')
        return redirect('users:dashboard')
    
    patient = request.user.patient
    
    medical_records = MedicalRecord.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient)
    lab_tests = LabTest.objects.filter(patient=patient)
    vaccinations = VaccinationRecord.objects.filter(patient=patient)
    
    timeline_events = []
    
    for record in medical_records:
        timeline_events.append({
            'date': record.created_at,
            'type': 'medical_record',
            'title': 'Medical Consultation',
            'description': record.diagnosis[:100] if len(record.diagnosis) > 100 else record.diagnosis,
            'icon': 'fa-stethoscope',
            'color': 'primary',
            'object': record,
        })
    
    for prescription in prescriptions:
        timeline_events.append({
            'date': prescription.created_at,
            'type': 'prescription',
            'title': f'Prescription: {prescription.medication_name}',
            'description': f'{prescription.dosage} - {prescription.frequency}',
            'icon': 'fa-pills',
            'color': 'success',
            'object': prescription,
        })
    
    for test in lab_tests:
        timeline_events.append({
            'date': test.ordered_date,
            'type': 'lab_test',
            'title': f'Lab Test: {test.test_name}',
            'description': f'Status: {test.get_status_display()}',
            'icon': 'fa-flask',
            'color': 'info',
            'object': test,
        })
    
    for vaccination in vaccinations:
        timeline_events.append({
            'date': vaccination.administration_date,
            'type': 'vaccination',
            'title': f'Vaccination: {vaccination.vaccine_name}',
            'description': f'Dose {vaccination.dose_number}',
            'icon': 'fa-syringe',
            'color': 'warning',
            'object': vaccination,
        })
    
    timeline_events.sort(key=lambda x: x['date'], reverse=True)
    
    context = {
        'timeline_events': timeline_events,
    }
    return render(request, 'medical_records/timeline.html', context)


@login_required
def doctor_my_patients(request):
    """
    Doctor's patient list - Shows ALL patients who have appointments with this doctor
    With working search functionality
    """
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can access this page.')
        return redirect('users:dashboard')
    
    doctor = request.user.doctor
    
    # Get ALL patients who have ANY appointments with this doctor (not just completed)
    patient_ids = Appointment.objects.filter(
        doctor=doctor
    ).values_list('patient_id', flat=True).distinct()
    
    # Get patient queryset
    patients = Patient.objects.filter(id__in=patient_ids).select_related('user')
    
    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        patients = patients.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__phone__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    # Add statistics for each patient
    patients_data = []
    for patient in patients:
        # Count total appointments with this doctor
        total_appointments = Appointment.objects.filter(
            patient=patient,
            doctor=doctor
        ).count()
        
        # Count medical records from this doctor
        total_records = MedicalRecord.objects.filter(
            patient=patient,
            doctor=doctor
        ).count()
        
        # Get last appointment date (any status)
        last_appointment = Appointment.objects.filter(
            patient=patient,
            doctor=doctor
        ).order_by('-appointment_date').first()
        
        # Get appointment status summary
        pending_count = Appointment.objects.filter(
            patient=patient,
            doctor=doctor,
            status='pending'
        ).count()
        
        confirmed_count = Appointment.objects.filter(
            patient=patient,
            doctor=doctor,
            status='confirmed'
        ).count()
        
        completed_count = Appointment.objects.filter(
            patient=patient,
            doctor=doctor,
            status='completed'
        ).count()
        
        patients_data.append({
            'id': patient.id,
            'patient': patient,
            'user': patient.user,
            'total_appointments': total_appointments,
            'total_records': total_records,
            'last_appointment': last_appointment.appointment_date if last_appointment else None,
            'last_appointment_status': last_appointment.get_status_display() if last_appointment else None,
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
            'completed_count': completed_count,
        })
    
    # Sort by most recent appointment
    patients_data.sort(key=lambda x: x['last_appointment'] if x['last_appointment'] else '1900-01-01', reverse=True)
    
    # Pagination
    paginator = Paginator(patients_data, 9)  # 9 patients per page
    page_number = request.GET.get('page', 1)
    patients_page = paginator.get_page(page_number)
    
    context = {
        'patients': patients_page,
        'total_patients': len(patients_data),
        'search_query': search_query,
    }
    
    return render(request, 'medical_records/doctor_my_patients.html', context)