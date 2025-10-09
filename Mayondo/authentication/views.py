from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from Wood.models import Add_user
from Wood.forms import Add_userForm
import logging

logger = logging.getLogger('authentication')


def landing_page(request):
    """Landing page view"""
    return render(request, 'authentication/index.html')


def login_view(request):
    """Proper login view with Django authentication"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # Clear any existing session data to prevent corruption
                    if hasattr(request, 'session'):
                        request.session.flush()
                    
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    logger.info(f'User {username} logged in successfully')
                    
                    # Redirect based on user role
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid username or password.')
                    logger.warning(f'Failed login attempt for username: {username}')
            except Exception as e:
                logger.error(f'Login error for user {username}: {str(e)}')
                messages.error(request, 'Login error occurred. Please try again.')
                # Clear session on error
                if hasattr(request, 'session'):
                    request.session.flush()
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'authentication/login.html')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = Add_userForm(request.POST)
        if form.is_valid():
            try:
                # Clear any existing session data to prevent corruption
                if hasattr(request, 'session'):
                    request.session.flush()
                
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created successfully for {username}!')
                logger.info(f'New user registered: {username}')
                
                # Automatically log in the user after registration
                login(request, user)
                return redirect('dashboard')
            except Exception as e:
                logger.error(f'Registration error for user {username}: {str(e)}')
                messages.error(request, 'Registration error occurred. Please try again.')
                # Clear session on error
                if hasattr(request, 'session'):
                    request.session.flush()
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = Add_userForm()
    
    return render(request, 'authentication/register.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('landing_page')
    
    return render(request, 'authentication/logout.html')


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'authentication/profile.html', {'user': request.user})