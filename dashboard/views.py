from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from railway.models import Train, Route, HaltStation, Station
from django.db.models import Q
from django.shortcuts import render, redirect
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

def TrainSchedule(request):
    context = {
        # 'trains': Train.objects.all(),
        'routes': Route.objects.all(),
        'halt_stations': HaltStation.objects.all().order_by('route', 'order')
    }
    return render(request, "dashboard/train_schedule.html", context)
def SearchTrains(request):
    routes = Route.objects.all()  # Display all routes by default
    stations = Station.objects.all()
    halt_stations = HaltStation.objects.all().order_by('route', 'order')

    source = None
    destination = None
    valid_routes = []

    if request.method == "POST":
        source_id = request.POST.get('source')
        destination_id = request.POST.get('destination')

        try:
            if source_id == destination_id and source_id is not None:
                messages.warning(request, 'Source and destination cannot be the same')
                return redirect('search_trains')

            source = Station.objects.get(id=source_id)
            destination = Station.objects.get(id=destination_id)

            # Direct routes between source and destination
            direct_routes = routes.filter(source=source, destination=destination)
            valid_routes.extend(direct_routes)

            for route in routes:
                source_halt = HaltStation.objects.filter(route=route, station=source).first()
                destination_halt = HaltStation.objects.filter(route=route, station=destination).first()

                # First Halt Station Case
                if source == route.source and destination_halt and destination_halt.order == 1:
                    valid_routes.append(route)

                # Last Halt Station Case
                if destination == route.destination and source_halt and source_halt.order == HaltStation.objects.filter(route=route).count():
                    valid_routes.append(route)

                # General Case: Both source and destination are halt stations
                if source_halt and destination_halt and source_halt.order < destination_halt.order:
                    valid_routes.append(route)

            # Remove duplicates
            valid_routes = list(set(valid_routes))

        except Station.DoesNotExist:
            messages.warning(request, 'Invalid source or destination station selected.')
            return redirect('search_trains')
        except Exception as e:
            messages.warning(request, f"Error: {e}")
            return redirect('search_trains')

    # If no valid search query, show all routes
    if not valid_routes:
        valid_routes = routes

    context = {
        'stations': stations,
        'routes': valid_routes,
        'halt_stations': halt_stations,
        'selected_source': source,
        'selected_destination': destination
    }

    return render(request, "dashboard/search_trains.html", context)


def TrainDetail(request, id):
    train = Train.objects.get(id=id)
    context = {
        'train': train
    }
    return render(request, "dashboard/train_detail.html", context)


@user_passes_test(is_passenger)
def PassengerProfilePage(request):
    return render(request, "dashboard/passenger_profile.html")

@user_passes_test(is_staff)
def StaffProfilePage(request):
    return render(request, "dashboard/staff_profile.html")
