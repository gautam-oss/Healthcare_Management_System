from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .forms import InsurancePredictionForm
from .models import InsurancePrediction
from .ml_model import predictor

@login_required
def predict_insurance(request):
    """Insurance cost prediction view"""
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can access the insurance predictor.')
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = InsurancePredictionForm(request.POST)
        if form.is_valid():
            # Get form data
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            bmi = form.cleaned_data['bmi']
            children = form.cleaned_data['children']
            smoker = form.cleaned_data['smoker']
            region = form.cleaned_data['region']
            
            try:
                # Make prediction
                predicted_cost = predictor.predict(age, sex, bmi, children, smoker, region)
                
                # Save prediction to database
                prediction = form.save(commit=False)
                prediction.user = request.user
                prediction.predicted_cost = predicted_cost
                prediction.save()
                
                # Redirect to result page
                return redirect('insurance:result', prediction_id=prediction.id)
                
            except Exception as e:
                messages.error(request, f'Error making prediction: {str(e)}')
    else:
        form = InsurancePredictionForm()
    
    return render(request, 'insurance/predict.html', {'form': form})

@login_required
def prediction_result(request, prediction_id):
    """Display prediction result"""
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can view prediction results.')
        return redirect('users:dashboard')
    try:
        prediction = InsurancePrediction.objects.get(id=prediction_id, user=request.user)
        
        # Get feature importance
        feature_importance = predictor.get_feature_importance()
        
        # Calculate risk factors
        risk_factors = []
        if prediction.smoker == 'yes':
            risk_factors.append({
                'factor': 'Smoking',
                'impact': 'Very High',
                'recommendation': 'Quitting smoking can significantly reduce insurance costs'
            })
        
        if prediction.bmi > 30:
            risk_factors.append({
                'factor': 'High BMI',
                'impact': 'High',
                'recommendation': 'Maintaining a healthy weight can lower costs'
            })
        elif prediction.bmi > 25:
            risk_factors.append({
                'factor': 'Overweight BMI',
                'impact': 'Moderate',
                'recommendation': 'Consider weight management for better rates'
            })
        
        if prediction.age > 50:
            risk_factors.append({
                'factor': 'Age',
                'impact': 'Moderate',
                'recommendation': 'Regular health checkups are important'
            })
        
        context = {
            'prediction': prediction,
            'feature_importance': feature_importance,
            'risk_factors': risk_factors,
        }
        
        return render(request, 'insurance/result.html', context)
        
    except InsurancePrediction.DoesNotExist:
        messages.error(request, 'Prediction not found.')
        return redirect('insurance:predict')

@login_required
def prediction_history(request):
    """View prediction history"""
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can view prediction history.')
        return redirect('users:dashboard')
    predictions = InsurancePrediction.objects.filter(user=request.user)
    
    # Calculate statistics
    if predictions.exists():
        avg_cost = predictions.aggregate(models.Avg('predicted_cost'))['predicted_cost__avg']
        min_cost = predictions.aggregate(models.Min('predicted_cost'))['predicted_cost__min']
        max_cost = predictions.aggregate(models.Max('predicted_cost'))['predicted_cost__max']
    else:
        avg_cost = min_cost = max_cost = None
    
    context = {
        'predictions': predictions,
        'avg_cost': avg_cost,
        'min_cost': min_cost,
        'max_cost': max_cost,
    }
    
    return render(request, 'insurance/history.html', context)

@login_required
def about_model(request):
    """Information about the ML model"""
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can view model information.')
        return redirect('users:dashboard')
    feature_importance = predictor.get_feature_importance()
    
    context = {
        'feature_importance': feature_importance,
    }
    
    return render(request, 'insurance/about.html', context)