from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import Customer
import hashlib

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = hashlib.sha256(form.cleaned_data['password'].encode()).hexdigest()
            
            try:
                customer = Customer.objects.get(email=email, password=password)
                request.session['customer_id'] = customer.id
                request.session['customer_name'] = customer.name
                messages.success(request, f'Welcome back, {customer.name}!')
                return redirect('book_list')
            except Customer.DoesNotExist:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('login')
