from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm
from users.models import Patient

# ✅ Helper function to check appointment conflicts
def check_appointment_conflict(doctor, appointment_date, appointment_time, exclude_id=None):
    """
    Check if doctor already has an appointment at this date/time
    """
    conflicts = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status__in=['pending', 'confirmed']  # Only check active appointments
    )
    
    # If updating an appointment, exclude it from conflict check
    if exclude_id:
        conflicts = conflicts.exclude(id=exclude_id)
    
    return conflicts.exists()

@login_required
def book_appointment(request):
    """Book a new appointment - WITH VALIDATION"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Only patients can book appointments.')
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            
            # Validate appointment date is not in the past
            if appointment.appointment_date < timezone.now().date():
                messages.error(request, 'Cannot book appointments in the past. Please select a future date.')
                return render(request, 'appointments/book.html', {'form': form})
            
            # Check if it's today and time has passed
            if appointment.appointment_date == timezone.now().date():
                current_time = timezone.now().time()
                if appointment.appointment_time < current_time:
                    messages.error(request, 'Cannot book appointments in the past. Please select a future time.')
                    return render(request, 'appointments/book.html', {'form': form})
            
            # Check for appointment conflicts
            if check_appointment_conflict(appointment.doctor, appointment.appointment_date, appointment.appointment_time):
                messages.error(
                    request, 
                    f'This time slot is already booked. Please choose another time or doctor.'
                )
                return render(request, 'appointments/book.html', {'form': form})
            
            # All validations passed - save the appointment
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments:success', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book.html', {'form': form})

@login_required
def my_appointments(request):
    """View user's appointments with statistics"""
    if hasattr(request.user, 'patient'):
        # Get appointments for patient
        appointments = Appointment.objects.filter(
            patient=request.user.patient
        ).select_related('doctor__user')
        
        # ✅ NEW: Calculate statistics for patient
        total_appointments = appointments.count()
        confirmed_count = appointments.filter(status='confirmed').count()
        pending_count = appointments.filter(status='pending').count()
        completed_count = appointments.filter(status='completed').count()
        
    elif hasattr(request.user, 'doctor'):
        # Get appointments for doctor
        appointments = Appointment.objects.filter(
            doctor=request.user.doctor
        ).select_related('patient__user')
        
        # ✅ NEW: Calculate statistics for doctor
        total_appointments = appointments.count()
        confirmed_count = appointments.filter(status='confirmed').count()
        pending_count = appointments.filter(status='pending').count()
        completed_count = appointments.filter(status='completed').count()
    else:
        appointments = []
        total_appointments = 0
        confirmed_count = 0
        pending_count = 0
        completed_count = 0
    
    context = {
        'appointments': appointments,
        'total_appointments': total_appointments,
        'confirmed_count': confirmed_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
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
    """Doctor can update appointment status - WITH VALIDATION"""
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
        
        # Validate status transitions
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        
        if new_status not in valid_statuses:
            messages.error(request, 'Invalid status selected.')
            return render(request, 'appointments/update.html', {'appointment': appointment})
        
        # Business logic validation
        if appointment.status == 'cancelled' and new_status == 'confirmed':
            messages.error(request, 'Cannot confirm a cancelled appointment. Please create a new one.')
            return render(request, 'appointments/update.html', {'appointment': appointment})
        
        if appointment.status == 'completed' and new_status == 'cancelled':
            messages.error(request, 'Cannot cancel a completed appointment.')
            return render(request, 'appointments/update.html', {'appointment': appointment})
        
        # Update the appointment
        appointment.status = new_status
        appointment.notes = notes
        appointment.save()
        
        messages.success(request, f'Appointment status updated to {appointment.get_status_display()}!')
        return redirect('appointments:my_appointments')
    
    return render(request, 'appointments/update.html', {'appointment': appointment})