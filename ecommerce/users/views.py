from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import logging

signup_logger = logging.getLogger('ecommerce.users.signup')
login_logger = logging.getLogger('ecommerce.users.login')
logout_logger = logging.getLogger('ecommerce.users.logout')

User = get_user_model()

# Create your views here.
def signup_view(request):
    if request.user.is_authenticated:
        signup_logger.debug("Authenticated user attempted to access signup page",extra={'user_id': request.user.id})
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            signup_logger.warning("Signup failed: password mismatch", extra={'username': username})
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            signup_logger.warning("Signup failed: username taken", extra={'username': username})
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            signup_logger.warning("Signup failed: email taken")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user, backend='users.backends.EmailBackend')
        signup_logger.info("User signed up successfully", extra={'user_id': user.id})

        return redirect('home')
    return render(request, 'users/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        login_logger.debug("Authenticated user attempted to access login page", extra={'user_id': request.user.id})
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email , password=password)

        if user is not None:
            login_logger.info("User logged in successfully", extra={'user_id': user.id})
            login(request, user, backend='users.backends.EmailBackend')
            return redirect('home')
        
        login_logger.warning("Login failed: invalid credentials")
        messages.error(request, "Invalid email or password.")
        return redirect('login')
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout_logger.info("User logged out successfully", extra={'user_id': request.user.id})
    logout(request)
    return redirect('home')