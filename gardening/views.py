from django.shortcuts import redirect
from django.contrib import messages

def custom_404(request, exception):
    messages.warning(request, "The page you're looking for doesn't exist. You've been redirected to the homepage.")
    return redirect('core:home') 