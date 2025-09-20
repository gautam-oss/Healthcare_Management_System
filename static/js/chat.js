// Chat functionality JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    // Auto-scroll to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Add message to chat
    function addMessage(content, isUser = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        
        const now = new Date();
        const timeString = now.toLocaleString();
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${isUser ? 'You' : 'AI Assistant'}:</strong> ${content.replace(/\n/g, '<br>')}
            </div>
            <div class="message-time">${timeString}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // Show typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        scrollToBottom();
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Get CSRF token
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    // Send message to backend
    async function sendMessage(message) {
        try {
            const response = await fetch('/chatbot/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (data.success) {
                addMessage(data.ai_response, false);
            } else {
                addMessage('Sorry, something went wrong. Please try again.', false);
                console.error('Chat error:', data.error);
            }
        } catch (error) {
            console.error('Network error:', error);
            addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection and try again.', false);
        } finally {
            hideTypingIndicator();
        }
    }

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, true);
        
        // Clear input
        messageInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send message to backend
        sendMessage(message);
    });

    // Handle Enter key press (without Shift)
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Auto-focus on input
    messageInput.focus();
    
    // Initial scroll to bottom
    scrollToBottom();
    
    // Handle input focus for mobile
    messageInput.addEventListener('focus', function() {
        setTimeout(scrollToBottom, 300);
    });
});

// Utility functions
function formatMessage(text) {
    // Convert URLs to clickable links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    text = text.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener">$1</a>');
    
    // Convert line breaks to HTML breaks
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// Handle page visibility change to maintain connection
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        // Re-focus input when page becomes visible
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.focus();
        }
    }
});