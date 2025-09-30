import numpy as np
import pickle
import os
from pathlib import Path

class InsuranceCostPredictor:
    """
    Insurance cost prediction model using Linear Regression
    Features: age, sex, bmi, children, smoker, region
    """
    
    def __init__(self):
        self.model = None
        self.model_path = Path(__file__).parent / 'trained_model.pkl'
        self.coefficients = None
        self.intercept = None
        
    def train_model(self):
        """
        Train a simple linear regression model with pre-calculated coefficients
        Based on typical insurance dataset patterns
        """
        # Pre-calculated coefficients based on insurance data analysis
        # These are approximate values that reflect realistic insurance cost factors
        self.coefficients = {
            'age': 256.85,           # Age has positive correlation
            'sex_male': -131.31,     # Males typically cost slightly less
            'bmi': 339.19,           # BMI has strong positive correlation
            'children': 475.50,      # More children increase cost
            'smoker_yes': 23848.53,  # Smoking is the strongest predictor
            'region_northwest': -352.96,
            'region_southeast': -1035.02,
            'region_southwest': -960.05,
        }
        self.intercept = -11938.54
        
        # Save the model
        self.save_model()
    
    def save_model(self):
        """Save the model coefficients"""
        model_data = {
            'coefficients': self.coefficients,
            'intercept': self.intercept
        }
        with open(self.model_path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self):
        """Load the model coefficients"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.coefficients = model_data['coefficients']
                self.intercept = model_data['intercept']
            return True
        return False
    
    def preprocess_features(self, age, sex, bmi, children, smoker, region):
        """
        Convert input features to model-ready format
        """
        features = {
            'age': float(age),
            'sex_male': 1.0 if sex.lower() == 'male' else 0.0,
            'bmi': float(bmi),
            'children': float(children),
            'smoker_yes': 1.0 if smoker.lower() == 'yes' else 0.0,
            'region_northwest': 1.0 if region.lower() == 'northwest' else 0.0,
            'region_southeast': 1.0 if region.lower() == 'southeast' else 0.0,
            'region_southwest': 1.0 if region.lower() == 'southwest' else 0.0,
        }
        return features
    
    def predict(self, age, sex, bmi, children, smoker, region):
        """
        Predict insurance cost based on input features
        """
        # Load model if not already loaded
        if self.coefficients is None:
            if not self.load_model():
                # Train model if it doesn't exist
                self.train_model()
        
        # Preprocess features
        features = self.preprocess_features(age, sex, bmi, children, smoker, region)
        
        # Calculate prediction
        prediction = self.intercept
        for feature_name, coefficient in self.coefficients.items():
            prediction += features[feature_name] * coefficient
        
        # Ensure prediction is not negative
        prediction = max(prediction, 1000.0)
        
        return round(prediction, 2)
    
    def get_feature_importance(self):
        """
        Return feature importance for visualization
        """
        if self.coefficients is None:
            self.load_model()
        
        importance = {
            'Smoking Status': abs(self.coefficients['smoker_yes']),
            'BMI': abs(self.coefficients['bmi']),
            'Age': abs(self.coefficients['age']),
            'Number of Children': abs(self.coefficients['children']),
            'Region': (abs(self.coefficients['region_northwest']) + 
                      abs(self.coefficients['region_southeast']) + 
                      abs(self.coefficients['region_southwest'])) / 3,
            'Sex': abs(self.coefficients['sex_male']),
        }
        
        # Sort by importance
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

# Initialize the predictor
predictor = InsuranceCostPredictor()

# Ensure model is trained on first import
if not predictor.load_model():
    predictor.train_model()