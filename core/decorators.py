from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def role_required(required_role):
    """
    Decorator to check if a user has the required role.
    Prevents redirect loops by skipping login/register pages.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            login_url = reverse('user_login')
            register_url = reverse('register')

            # Allow public pages (login and register) to be accessed without checks
            if request.path in [login_url, register_url]:
                return view_func(request, *args, **kwargs)

            # User not authenticated -> redirect to login
            if not request.user.is_authenticated:
                messages.error(request, 'You must log in first!')
                return redirect('user_login')

            # Check user role
            if hasattr(request.user, 'userprofile'):
                role = request.user.userprofile.role
                role_hierarchy = {'viewer': 1, 'editor': 2, 'admin': 3}
                if role_hierarchy.get(role, 0) >= role_hierarchy.get(required_role, 0):
                    return view_func(request, *args, **kwargs)

            # Role not sufficient -> redirect to home
            messages.error(request, 'You do not have permission to access this page!')
            return redirect('home')

        return wrapper
    return decorator

# Convenience decorators
viewer_required = role_required('viewer')
editor_required = role_required('editor')
admin_required = role_required('admin')