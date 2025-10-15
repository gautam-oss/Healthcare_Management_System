from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm
from users.models import Patient

@login_required
def book_appointment(request):
    """Book a new appointment"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Only patients can book appointments.')
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments:success', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book.html', {'form': form})

@login_required
def my_appointments(request):
    """View user's appointments with real status counts"""
    if hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(
            patient=request.user.patient
        ).select_related('doctor__user')
        
        # Calculate real status counts for patient
        confirmed_count = appointments.filter(status='confirmed').count()
        pending_count = appointments.filter(status='pending').count()
        completed_count = appointments.filter(status='completed').count()
        cancelled_count = appointments.filter(status='cancelled').count()
        
    elif hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(
            doctor=request.user.doctor
        ).select_related('patient__user')
        
        # Calculate real status counts for doctor
        confirmed_count = appointments.filter(status='confirmed').count()
        pending_count = appointments.filter(status='pending').count()
        completed_count = appointments.filter(status='completed').count()
        cancelled_count = appointments.filter(status='cancelled').count()
    else:
        appointments = []
        confirmed_count = pending_count = completed_count = cancelled_count = 0
    
    context = {
        'appointments': appointments,
        'confirmed_count': confirmed_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
    }
    
    return render(request, 'appointments/list.html', context)

@login_required
def appointment_success(request, appointment_id):
    """Appointment booking success page"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Make sure user can only see their own appointment
    if hasattr(request.user, 'patient') and appointment.patient != request.user.patient:
        messages.error(request, 'You can only view your own appointments.')
        return redirect('appointments:my_appointments')
    
    return render(request, 'appointments/success.html', {'appointment': appointment})

@login_required
def update_appointment(request, appointment_id):
    """Doctor can update appointment status"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Only doctors can update appointments
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can update appointments.')
        return redirect('appointments:my_appointments')
    
    # Only the assigned doctor can update
    if appointment.doctor != request.user.doctor:
        messages.error(request, 'You can only update your own appointments.')
        return redirect('appointments:my_appointments')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
            old_status = appointment.status
            appointment.status = new_status
            appointment.notes = notes
            appointment.save()
            
            messages.success(request, f'Appointment status updated from {old_status} to {new_status}!')
            return redirect('appointments:my_appointments')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return render(request, 'appointments/update.html', {'appointment': appointment})