import google.generativeai as genai
from django.conf import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Configure Gemini AI
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")

def get_gemini_response(user_message, conversation_history=None):
    """
    Get response from Gemini AI using Gemini 1.5 Flash
    """
    try:
        # Create the model - using gemini-1.5-flash for better performance
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create healthcare context
        healthcare_context = """
        You are a helpful healthcare assistant for a Healthcare Management System. 
        You can help with:
        - General health information and tips
        - Explaining medical terms and conditions
        - Appointment scheduling guidance
        - Symptom information (but always recommend consulting a doctor)
        - Medication information (general, non-prescription advice only)
        - Healthy lifestyle recommendations
        - Preventive care information
        
        Important guidelines:
        - Always remind users to consult with healthcare professionals for medical advice
        - Do not provide specific medical diagnoses
        - Do not recommend prescription medications
        - Keep responses friendly, helpful, and informative
        - If asked about emergency situations, advise to seek immediate medical attention
        - Provide accurate, evidence-based health information
        
        Keep your responses concise but comprehensive, and always prioritize user safety.
        """
        
        # Prepare the prompt with conversation context
        if conversation_history and len(conversation_history) > 0:
            # Include recent conversation history for context (last 5 messages)
            recent_history = list(conversation_history)[-5:] if len(conversation_history) > 5 else list(conversation_history)
            history_text = "\n".join([
                f"{'User' if msg.is_from_user else 'Assistant'}: {msg.content[:500]}..."  # Limit message length
                for msg in recent_history
            ])
            prompt = f"{healthcare_context}\n\nRecent conversation:\n{history_text}\n\nCurrent User Question: {user_message}\n\nAssistant Response:"
        else:
            prompt = f"{healthcare_context}\n\nUser Question: {user_message}\n\nAssistant Response:"
        
        # Configure generation parameters for better responses
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,  # Balanced creativity and accuracy
            top_p=0.9,
            top_k=40,
            max_output_tokens=1000,  # Reasonable response length
        )
        
        # Safety settings
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Check if response was generated successfully
        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()
        else:
            logger.warning("Gemini API returned empty response")
            return "I apologize, but I'm having trouble generating a response right now. Could you please try rephrasing your question?"
        
    except Exception as e:
        logger.error(f"Error getting Gemini response: {e}")
        
        # Return different error messages based on the type of error
        if "API_KEY" in str(e).upper():
            return "I'm experiencing authentication issues. Please contact support if this problem persists."
        elif "QUOTA" in str(e).upper() or "LIMIT" in str(e).upper():
            return "I'm currently experiencing high traffic. Please try again in a moment."
        elif "SAFETY" in str(e).upper():
            return "I understand you're looking for health information, but I need to be careful with my responses. Could you please rephrase your question?"
        else:
            return "I apologize, but I'm having trouble connecting to my AI service right now. Please try again later or contact support if the issue persists."

def validate_api_key():
    """
    Validate if the Gemini API key is properly configured
    """
    try:
        if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
            return False, "GEMINI_API_KEY not found in settings"
        
        # Try a simple API call to validate the key
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Hello", 
            generation_config=genai.types.GenerationConfig(max_output_tokens=10))
        
        if response and hasattr(response, 'text'):
            return True, "API key is valid"
        else:
            return False, "API key validation failed"
            
    except Exception as e:
        return False, f"API key validation error: {e}"