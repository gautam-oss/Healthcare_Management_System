from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Conversation, Message
from .services import get_gemini_response

@login_required
def chat_page(request):
    """Main chat page - don't load messages here"""
    return render(request, 'chatbot/chat.html')

@login_required
@require_http_methods(["GET"])
def chat_history(request):
    """Get chat history as JSON"""
    try:
        # Get or create conversation for this user
        conversation, created = Conversation.objects.get_or_create(
            user=request.user,
            defaults={'user': request.user}
        )
        
        # Get recent messages (last 20 to avoid overloading)
        messages = conversation.messages.all()[:20]
        
        # Convert to JSON-serializable format
        messages_data = []
        for msg in messages:
            messages_data.append({
                'content': msg.content,
                'is_from_user': msg.is_from_user,
                'created_at': msg.created_at.isoformat(),
            })
        
        return JsonResponse({
            'success': True,
            'messages': messages_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Handle chat messages via AJAX"""
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

@login_required
@require_http_methods(["POST"])
def clear_chat(request):
    """Clear chat history for the current user"""
    try:
        conversation = Conversation.objects.filter(user=request.user).first()
        if conversation:
            conversation.messages.all().delete()
            
        return JsonResponse({'success': True, 'message': 'Chat history cleared'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})