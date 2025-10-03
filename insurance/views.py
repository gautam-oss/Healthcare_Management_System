from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .forms import InsurancePredictionForm
from .models import InsurancePrediction
from .ml_model import predictor

def predict_insurance(request):
    """
    Insurance cost prediction view - PUBLIC ACCESS
    Anyone can use it, but only logged-in users can save history
    """
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
                
                # Save prediction only for logged-in users
                if request.user.is_authenticated:
                    prediction = form.save(commit=False)
                    prediction.user = request.user
                    prediction.predicted_cost = predicted_cost
                    prediction.save()
                    
                    # Redirect to result page
                    return redirect('insurance:result', prediction_id=prediction.id)
                else:
                    # For guest users, show result directly without saving
                    # Store in session temporarily
                    request.session['guest_prediction'] = {
                        'age': age,
                        'sex': sex,
                        'bmi': float(bmi),
                        'children': children,
                        'smoker': smoker,
                        'region': region,
                        'predicted_cost': float(predicted_cost)
                    }
                    return redirect('insurance:guest_result')
                
            except Exception as e:
                messages.error(request, f'Error making prediction: {str(e)}')
    else:
        form = InsurancePredictionForm()
    
    return render(request, 'insurance/predict.html', {'form': form})

def prediction_result(request, prediction_id):
    """
    Display prediction result - REQUIRES LOGIN
    """
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view saved predictions.')
        return redirect('users:login')
    
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

def guest_result(request):
    """
    Display prediction result for guest users - PUBLIC ACCESS
    """
    guest_prediction = request.session.get('guest_prediction')
    
    if not guest_prediction:
        messages.error(request, 'No prediction data found. Please make a prediction first.')
        return redirect('insurance:predict')
    
    # Get feature importance
    feature_importance = predictor.get_feature_importance()
    
    # Calculate risk factors
    risk_factors = []
    if guest_prediction['smoker'] == 'yes':
        risk_factors.append({
            'factor': 'Smoking',
            'impact': 'Very High',
            'recommendation': 'Quitting smoking can significantly reduce insurance costs'
        })
    
    if guest_prediction['bmi'] > 30:
        risk_factors.append({
            'factor': 'High BMI',
            'impact': 'High',
            'recommendation': 'Maintaining a healthy weight can lower costs'
        })
    elif guest_prediction['bmi'] > 25:
        risk_factors.append({
            'factor': 'Overweight BMI',
            'impact': 'Moderate',
            'recommendation': 'Consider weight management for better rates'
        })
    
    if guest_prediction['age'] > 50:
        risk_factors.append({
            'factor': 'Age',
            'impact': 'Moderate',
            'recommendation': 'Regular health checkups are important'
        })
    
    context = {
        'prediction': guest_prediction,
        'feature_importance': feature_importance,
        'risk_factors': risk_factors,
        'is_guest': True,
    }
    
    return render(request, 'insurance/result.html', context)

@login_required
def prediction_history(request):
    """
    View prediction history - REQUIRES LOGIN
    """
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

def about_model(request):
    """
    Information about the ML model - PUBLIC ACCESS
    """
    feature_importance = predictor.get_feature_importance()
    
    context = {
        'feature_importance': feature_importance,
    }
    
    return render(request, 'insurance/about.html', context)