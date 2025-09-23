from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientRegistrationForm, DoctorRegistrationForm

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
    """User dashboard"""
    context = {
        'user': request.user,
    }
    
    if hasattr(request.user, 'patient'):
        context['profile'] = request.user.patient
        context['profile_type'] = 'patient'
    elif hasattr(request.user, 'doctor'):
        context['profile'] = request.user.doctor
        context['profile_type'] = 'doctor'
    
    return render(request, 'users/dashboard.html', context)

def custom_logout(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('users:login')