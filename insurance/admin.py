from django.contrib import admin
from .models import InsurancePrediction

@admin.register(InsurancePrediction)
class InsurancePredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'bmi', 'smoker', 'predicted_cost', 'created_at')
    list_filter = ('smoker', 'region', 'created_at')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Personal Details', {
            'fields': ('age', 'sex', 'bmi', 'children')
        }),
        ('Health & Location', {
            'fields': ('smoker', 'region')
        }),
        ('Prediction', {
            'fields': ('predicted_cost', 'created_at')
        }),
    )