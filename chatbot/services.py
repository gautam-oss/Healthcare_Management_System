import google.generativeai as genai
from django.conf import settings

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_gemini_response(user_message, conversation_history=None):
    """
    Get response from Gemini AI
    """
    try:
        # Create the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Create healthcare context
        healthcare_context = """
        You are a helpful healthcare assistant for a Healthcare Management System. 
        You can help with:
        - General health information and tips
        - Explaining medical terms
        - Appointment scheduling guidance
        - Symptom information (but always recommend consulting a doctor)
        
        Important: Always remind users to consult with healthcare professionals for medical advice.
        Keep responses friendly, helpful, and informative.
        """
        
        # Prepare the prompt
        if conversation_history:
            # Include recent conversation history for context
            history_text = "\n".join([
                f"{'User' if msg.is_from_user else 'Assistant'}: {msg.content}"
                for msg in conversation_history[-5:]  # Last 5 messages for context
            ])
            prompt = f"{healthcare_context}\n\nRecent conversation:\n{history_text}\n\nUser: {user_message}\n\nAssistant:"
        else:
            prompt = f"{healthcare_context}\n\nUser: {user_message}\n\nAssistant:"
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "I apologize, but I'm having trouble connecting to my AI service right now. Please try again later or contact support if the issue persists."
