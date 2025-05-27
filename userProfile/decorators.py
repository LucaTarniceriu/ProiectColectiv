from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def user_type_required(required_type):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == required_type:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied  
        return _wrapped_view
    return decorator
