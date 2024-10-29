from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .models import User_client  # Ensure this is the correct import
from django.contrib.auth import logout
from django.contrib import messages  # Import messages for the messaging framework
def signup_login_view(request):
    # Render the login/signup page
    return render(request, 'animated-login/login.html')



def signup(request):
    if request.method == 'POST':  
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('adress')  # Fixed spelling
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')
        
        hashed_password = make_password(password)

        if not User_client.objects.filter(username=username).exists():  # Ensure you're using User_client
            User_client.objects.create(username=username, email=email, phone_number=phone_number, address=address,
                                       date_of_birth=date_of_birth, password=hashed_password)
            messages.success(request, "Signup successful! Please log in.")  # Set a success message
            return redirect('auth')
        else:
            messages.error(request, "Username already exists.")  # Set an error message
            return redirect('auth')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User_client.objects.get(username=username)  # Ensure you're using User_client
            if check_password(password, user.password):
                request.session['user_id'] = user.id  # Setting session for logged-in user
                # messages.success(request, "Login successful!")  # Set a success message               
                return redirect('front',user)
            else:
                messages.error(request, "Invalid password.")  # Set an error message
                return redirect('auth')
        except User_client.DoesNotExist:
            messages.error(request, "User does not exist.")  # Set an error message
            return redirect('auth')

def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out.")  # Set a success message
    return redirect('auth')
