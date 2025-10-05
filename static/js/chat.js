// ✅ FIXED: Enhanced chat.js with proper CSRF token handling

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const typingIndicator = document.getElementById('typingIndicator');

    console.log('Chat system initialized');

    // Auto-scroll to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Add message to chat with better formatting
    function addMessage(content, isUser = true) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        
        const now = new Date();
        const timeString = now.toLocaleString();
        
        // Sanitize content and convert newlines
        const sanitizedContent = content
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/\n/g, '<br>');
        
        messageDiv.innerHTML = `
            <div class="message-wrapper">
                <div class="message-sender">
                    ${isUser ? '<i class="fas fa-user-circle"></i> You' : '<i class="fas fa-robot"></i> AI Assistant'}
                </div>
                <div class="message-content">
                    <div class="message-text">${sanitizedContent}</div>
                </div>
                <div class="message-time">
                    <i class="far fa-clock me-1"></i>
                    ${timeString}
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // Show/hide typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        scrollToBottom();
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // ✅ FIXED: Get CSRF token from cookie (proper Django way)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ✅ FIXED: Get CSRF token (supports both methods)
    function getCSRFToken() {
        // First try to get from cookie
        let token = getCookie('csrftoken');
        
        // If not in cookie, get from form token
        if (!token) {
            const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
            token = tokenInput ? tokenInput.value : '';
        }
        
        return token;
    }

    // Enhanced message sending with proper CSRF handling
    async function sendMessage(message) {
        console.log('Sending message:', message);
        
        try {
            const csrfToken = getCSRFToken();
            
            if (!csrfToken) {
                throw new Error('CSRF token not found. Please refresh the page.');
            }

            const response = await fetch('/chatbot/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,  // ✅ FIXED: Proper CSRF header
                },
                body: JSON.stringify({ message: message })
            });

            console.log('Response status:', response.status);
            
            // Handle different response statuses
            if (!response.ok) {
                if (response.status === 403) {
                    throw new Error('Session expired. Please refresh the page.');
                } else if (response.status === 500) {
                    throw new Error('Server error. Please try again later.');
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            }

            const data = await response.json();
            console.log('Response data:', data);

            if (data.success) {
                addMessage(data.ai_response, false);
                
                // Show helpful message for guests
                if (!data.is_authenticated) {
                    console.log('Guest mode - conversation not saved');
                }
            } else {
                console.error('API Error:', data.error);
                addMessage(`Error: ${data.error || 'Something went wrong'}`, false);
                
                // Show debug info for superusers
                if (data.debug) {
                    console.error('Debug info:', data.debug);
                }
            }
        } catch (error) {
            console.error('Network/Parse error:', error);
            
            let errorMessage = 'Sorry, I encountered an error. ';
            
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                errorMessage += 'Please check your internet connection.';
            } else if (error.message.includes('CSRF')) {
                errorMessage += 'Please refresh the page and try again.';
            } else {
                errorMessage += error.message;
            }
            
            addMessage(errorMessage, false);
        } finally {
            hideTypingIndicator();
        }
    }

    // Form submission handler
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) {
            console.log('Empty message, ignoring');
            return;
        }

        console.log('Form submitted with message:', message);

        // Add user message to chat
        addMessage(message, true);
        
        // Clear input and show typing indicator
        messageInput.value = '';
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

    // ✅ NEW: Test connection on page load
    console.log('Chat system ready!');
    console.log('CSRF Token available:', getCSRFToken() ? 'Yes' : 'No');
});

// Page visibility handling
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.focus();
        }
    }
});