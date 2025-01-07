from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

#decorators
def is_passenger(user):
    return hasattr(user, 'is_passenger') and user.is_passenger

def is_staff(user):
    return hasattr(user, 'is_staff') and user.is_staff


#views
def index(request):
    messages.success(request, 'Welcome to the dashboard')
    return render(request, "dashboard/index.html")

def profile(request):
    if request.user.is_staff:
        return redirect('staff_profile')
    else:
        return redirect('passenger_profile')
    
@user_passes_test(is_passenger)
def PassengerProfilePage(request):
    return render(request, "dashboard/passenger_profile.html")

@user_passes_test(is_staff)
def StaffProfilePage(request):
    return render(request, "dashboard/staff_profile.html")

def SearchTrains(request):
    return render(request, "dashboard/search_trains.html")