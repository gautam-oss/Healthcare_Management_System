from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Conversation, Message
from .services import get_gemini_response
from django.contrib import messages

@login_required
def chat_page(request):
    """Main chat page - don't load messages here"""
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can access the chatbot.')
        return redirect('users:dashboard')
    return render(request, 'chatbot/chat.html')

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Handle chat messages via AJAX"""
    if request.user.user_type != 'patient':
        return JsonResponse({'error': 'Only patients can send messages.'}, status=403)
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Limit message length
        if len(user_message) > 1000:
            return JsonResponse({'error': 'Message too long. Please limit to 1000 characters.'}, status=400)
        
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
        
        # Get conversation history for context (last 10 messages)
        recent_messages = conversation.messages.all()[:10]
        
        # Get AI response
        ai_response = get_gemini_response(user_message, recent_messages)
        
        # Save AI response
        ai_msg = Message.objects.create(
            conversation=conversation,
            content=ai_response,
            is_from_user=False
        )
        
        # Update conversation timestamp
        conversation.save()  # This updates the updated_at field
        
        return JsonResponse({
            'success': True,
            'ai_response': ai_response,
            'user_message_id': user_msg.id,
            'ai_message_id': ai_msg.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print(f"Chat error: {e}")  # For debugging
        return JsonResponse({
            'error': 'Something went wrong. Please try again.',
            'debug': str(e) if request.user.is_superuser else None
        }, status=500)