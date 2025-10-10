from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientRegistrationForm, DoctorRegistrationForm
from appointments.models import Appointment
from chatbot.models import Conversation
from insurance.models import InsurancePrediction

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
    """User dashboard with real-time statistics"""
    context = {
        'user': request.user,
    }
    
    if hasattr(request.user, 'patient'):
        context['profile'] = request.user.patient
        context['profile_type'] = 'patient'
        
        # ✅ NEW: Calculate patient statistics
        context['total_appointments'] = Appointment.objects.filter(
            patient=request.user.patient
        ).count()
        
        # Count AI conversations (messages sent by user)
        try:
            conversation = Conversation.objects.get(user=request.user)
            context['ai_conversations'] = conversation.messages.filter(
                is_from_user=True
            ).count()
        except Conversation.DoesNotExist:
            context['ai_conversations'] = 0
        
        # Count insurance predictions
        context['insurance_predictions'] = InsurancePrediction.objects.filter(
            user=request.user
        ).count()
        
    elif hasattr(request.user, 'doctor'):
        context['profile'] = request.user.doctor
        context['profile_type'] = 'doctor'
        
        # ✅ NEW: Calculate doctor statistics
        context['total_appointments'] = Appointment.objects.filter(
            doctor=request.user.doctor
        ).count()
        
        context['pending_appointments'] = Appointment.objects.filter(
            doctor=request.user.doctor,
            status='pending'
        ).count()
        
        context['confirmed_appointments'] = Appointment.objects.filter(
            doctor=request.user.doctor,
            status='confirmed'
        ).count()
    
    return render(request, 'users/dashboard.html', context)