"""
URL helper utilities for handling both token-based and session-based URLs.
This ensures backward compatibility while providing seamless access.
"""

from django.urls import reverse
from django.contrib.auth import get_user_model
from .tokens import make_dashboard_token
from ..models import UserProfile

User = get_user_model()


def get_user_token(request):
    """
    Get the user's dashboard token from session, or generate one if it doesn't exist.
    Returns None if user is not authenticated.
    """
    if not request.user.is_authenticated:
        return None
    
    token = request.session.get('dashboard_token')
    if not token:
        try:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            token = make_dashboard_token(profile)
            request.session['dashboard_token'] = token
            request.session.save()
        except Exception:
            return None
    
    return token


def get_user_role(request):
    """
    Get the user's role from their profile.
    Returns None if user is not authenticated or has no profile.
    """
    if not request.user.is_authenticated:
        return None
    
    try:
        profile = UserProfile.objects.get(user=request.user)
        return profile.role
    except Exception:
        return None


def reverse_with_token(request, url_name, *args, **kwargs):
    """
    Generate a URL that works with both token-based and session-based access.
    If token is available, uses token-based URL. Otherwise, uses session-based URL.
    
    Args:
        request: The current request object
        url_name: The URL name to reverse
        *args: Positional arguments for the URL
        **kwargs: Keyword arguments for the URL
    
    Returns:
        The appropriate URL string
    """
    # Check if this is a token-based URL name
    if url_name.endswith('_session'):
        # This is already a session-based URL, use it directly
        return reverse(url_name, args=args, kwargs=kwargs)
    
    # Try to get token and role
    token = get_user_token(request)
    role = get_user_role(request)
    
    if token and role:
        # Use token-based URL - add token and role to kwargs if they're required
        # Check if this URL pattern requires token and role parameters by trying to reverse it
        try:
            return reverse(url_name, args=args, kwargs=kwargs)
        except:
            # If it fails, try adding token and role parameters
            kwargs['token'] = token
            kwargs['role'] = role
            try:
                return reverse(url_name, args=args, kwargs=kwargs)
            except:
                # If still fails, fall back to session-based URL
                session_url_name = f"{url_name}_session"
                try:
                    return reverse(session_url_name, args=args, kwargs=kwargs)
                except:
                    # Last resort - try original URL without token/role
                    kwargs.pop('token', None)
                    kwargs.pop('role', None)
                    return reverse(url_name, args=args, kwargs=kwargs)
    else:
        # Use session-based URL
        session_url_name = f"{url_name}_session"
        try:
            return reverse(session_url_name, args=args, kwargs=kwargs)
        except:
            # Fallback to original URL if session version doesn't exist
            return reverse(url_name, args=args, kwargs=kwargs)


def get_dashboard_url(request):
    """
    Get the appropriate dashboard URL for the current user.
    Returns token-based URL if available, otherwise session-based URL.
    """
    token = get_user_token(request)
    role = get_user_role(request)
    
    if token and role:
        return reverse('dashboard_signed_with_role', kwargs={'token': token, 'role': role})
    else:
        return reverse('dashboard_session')


def get_project_list_url(request):
    """
    Get the appropriate project list URL for the current user.
    """
    return reverse_with_token(request, 'project_list')


def get_project_view_url(request, project_source, project_id):
    """
    Get the appropriate project view URL for the current user.
    """
    return reverse_with_token(request, 'project_view', project_source=project_source, pk=project_id)


def get_task_list_url(request, project_id):
    """
    Get the appropriate task list URL for the current user.
    """
    return reverse_with_token(request, 'task_list', project_id=project_id)


def get_gantt_view_url(request, project_id):
    """
    Get the appropriate Gantt view URL for the current user.
    """
    return reverse_with_token(request, 'task_gantt_view', project_id=project_id)
