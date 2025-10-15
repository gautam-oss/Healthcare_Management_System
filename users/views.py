from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from appointments.models import Appointment
from chatbot.models import Conversation
from insurance.models import InsurancePrediction
from medical_records.models import MedicalRecord

def register_patient(request):
    """Patient registration view"""
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Healthcare Management System.')
            return redirect('users:dashboard')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'users/register.html', {
        'form': form,
        'user_type': 'Patient'
    })

def register_doctor(request):
    """Doctor registration view"""
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome Dr. {}!'.format(user.get_full_name()))
            return redirect('users:dashboard')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'users/register.html', {
        'form': form,
        'user_type': 'Doctor'
    })

@login_required
def dashboard(request):
    """User dashboard with real database counts"""
    context = {
        'user': request.user,
    }
    
    if hasattr(request.user, 'patient'):
        # PATIENT DASHBOARD
        context['profile'] = request.user.patient
        context['profile_type'] = 'patient'
        
        # Count real data from database
        context['total_appointments'] = Appointment.objects.filter(
            patient=request.user.patient
        ).count()
        
        context['total_records'] = MedicalRecord.objects.filter(
            patient=request.user.patient
        ).count()
        
        # Count conversations (AI chats)
        try:
            conversation = Conversation.objects.get(user=request.user)
            context['chat_count'] = conversation.messages.count()
        except Conversation.DoesNotExist:
            context['chat_count'] = 0
        
        # Count insurance predictions
        context['prediction_count'] = InsurancePrediction.objects.filter(
            user=request.user
        ).count()
        
    elif hasattr(request.user, 'doctor'):
        # DOCTOR DASHBOARD
        context['profile'] = request.user.doctor
        context['profile_type'] = 'doctor'
        
        # Count consultations (all appointments)
        context['total_appointments'] = Appointment.objects.filter(
            doctor=request.user.doctor
        ).count()
        
        # Count unique patients (from completed appointments)
        from django.db.models import Count
        context['total_records'] = Appointment.objects.filter(
            doctor=request.user.doctor,
            status='completed'
        ).values('patient').distinct().count()
        
        # Count pending appointments
        context['chat_count'] = Appointment.objects.filter(
            doctor=request.user.doctor,
            status='pending'
        ).count()
        
        # Count completed appointments
        context['prediction_count'] = Appointment.objects.filter(
            doctor=request.user.doctor,
            status='completed'
        ).count()
    
    return render(request, 'users/dashboard.html', context)