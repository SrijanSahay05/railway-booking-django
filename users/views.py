from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages


# Create your views here.
def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        print(f"Received POST request with username: {username}")
        if password != confirm_password:
            return render(request, 'users/register.html', {'message': 'Passwords do not match'})
        try:
            user = CustomUser.objects.create(username=username, email=email, password=make_password(password), user_type=user_type)
            user.set_password(password)
            user.save()
            print(f"User {username} created successfully")
            messages.success(request, f"User {username} created successfully")
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    print(f"Authentication successful for user: {username}")
                    login(request, user)
                    messages.success(request, f"Welcome {username}")
                    return redirect('index')  # Redirect to the dashboard
            except Exception as e:
                print(f"An error occurred during authentication: {str(e)}")
                messages.error(request, f'An error occurred: {str(e)}')
            return redirect('index')  # Redirect to the dashboard
        except Exception as e:
            print(f"An error occurred during user creation: {str(e)}")
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'users/register.html', {'message': f'An error occurred: {str(e)}'})
    print("Received GET request")
    context = {}
    return render(request, 'users/register.html', context)    

        
def LoginView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Received POST request with username: {username}")
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(f"Authentication successful for user: {username}")
                login(request, user)
                return redirect('index')  # Redirect to the dashboard
            else:
                print(f"Authentication failed for user: {username}")
                return render(request, 'users/login.html', {'message': 'Invalid credentials'})
        except Exception as e:
            print(f"An error occurred during authentication: {str(e)}")
            return render(request, 'users/login.html', {'message': f'An error occurred: {str(e)}'})

    print("Received GET request")
    context = {}
    return render(request, 'users/login.html', context)

def LogoutView(request):
    print(f"Logging out user: {request.user.username}")
    logout(request)
    return redirect('index')  # Redirect to the dashboard