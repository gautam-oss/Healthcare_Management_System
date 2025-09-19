from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('appointments/', include('appointments.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('', lambda request: redirect('users:login')),  # Redirect home to login
]