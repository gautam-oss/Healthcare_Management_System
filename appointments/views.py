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
    """View user's appointments"""
    if hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient)
    elif hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
    else:
        appointments = []
    
    return render(request, 'appointments/list.html', {'appointments': appointments})

@login_required
def appointment_success(request, appointment_id):
    """Appointment booking success page"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Make sure user can only see their own appointment
    if hasattr(request.user, 'patient') and appointment.patient != request.user.patient:
        messages.error(request, 'You can only view your own appointments.')
        return redirect('appointments:my_appointments')
    
    return render(request, 'appointments/success.html', {'appointment': appointment})
