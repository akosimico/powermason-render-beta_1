from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import UserProfile
from .utils.tokens import make_dashboard_token

User = get_user_model()

class LimitMessagesMiddleware:
    """Middleware to limit the number of messages stored"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Limit messages to the last 3
        storage = messages.get_messages(request)
        message_list = list(storage)
        
        if len(message_list) > 3:
            # Clear all messages
            storage.used = False
            # Re-add only the last 3
            for message in message_list[-3:]:
                messages.add_message(request, message.level, message.message, message.tags)
        
        return response


class TokenGenerationMiddleware:
    """
    Middleware to automatically generate dashboard tokens for authenticated users
    who don't have them in their session. This ensures seamless access even when
    users come from URLs without tokens.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only process authenticated users
        if request.user.is_authenticated:
            # Check if user has a dashboard token in session
            if 'dashboard_token' not in request.session:
                try:
                    # Get or create user profile
                    profile, created = UserProfile.objects.get_or_create(user=request.user)
                    
                    # Generate a new token
                    token = make_dashboard_token(profile)
                    
                    # Store token in session
                    request.session['dashboard_token'] = token
                    request.session.save()
                    
                except Exception as e:
                    # Log error but don't break the request
                    print(f"Error generating dashboard token: {e}")
        
        response = self.get_response(request)
        return response