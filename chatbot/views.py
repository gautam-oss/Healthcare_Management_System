from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Conversation, Message
from .services import get_gemini_response

@login_required
def chat_page(request):
    """Main chat page"""
    # Get or create conversation for this user
    conversation, created = Conversation.objects.get_or_create(
        user=request.user,
        defaults={'user': request.user}
    )
    
    # Get recent messages
    messages = conversation.messages.all()[:50]  # Last 50 messages
    
    return render(request, 'chatbot/chat.html', {
        'conversation': conversation,
        'messages': messages
    })

@csrf_exempt
@login_required
def send_message(request):
    """Handle chat messages via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create conversation
        conversation, created = Conversation.objects.get_or_create(
            user=request.user,
            defaults={'user': request.user}
        )
        
        # Save user message
        user_msg = Message.objects.create(
            conversation=conversation,
            content=user_message,
            is_from_user=True
        )
        
        # Get conversation history for context
        recent_messages = conversation.messages.all()[:10]  # Last 10 messages
        
        # Get AI response
        ai_response = get_gemini_response(user_message, recent_messages)
        
        # Save AI response
        ai_msg = Message.objects.create(
            conversation=conversation,
            content=ai_response,
            is_from_user=False
        )
        
        return JsonResponse({
            'success': True,
            'ai_response': ai_response,
            'message_id': ai_msg.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Chat error: {e}")
        return JsonResponse({'error': 'Something went wrong. Please try again.'}, status=500)
