from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),                    # Home page (NEW)
    path('users/', include('users.urls')),             # User auth
    path('appointments/', include('appointments.urls')),# Appointments
    path('chatbot/', include('chatbot.urls')),         # Chatbot
    path('insurance/', include('insurance.urls')),     # Insurance
    path('medical-records/', include('medical_records.urls')),  # ADD THIS LINE
]

# Add this for media files (if not already present)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)