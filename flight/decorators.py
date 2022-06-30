from django.shortcuts import redirect

# Create your decorators here.

def restriction(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper
