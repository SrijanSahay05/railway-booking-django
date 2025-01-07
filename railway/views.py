from django.shortcuts import render
from .models import Route, Station, HaltStation
from datetime import timedelta
from django.contrib import messages



def AddTrain(request):
    stations = Station.objects.all()
    routes = Route.objects.all()
    if request.method == "POST":
        if "add_train" in request.POST:
            print("Received POST request for add_train")
            route_name = request.POST.get('route_name')
            route_number = request.POST.get('route_number')
            route_source_code = request.POST.get('route_source')
            route_destination_code = request.POST.get('route_destination')
            route_base_fare = request.POST.get('route_base_fare')
            route_departure_time = request.POST.get('route_departure_time')
            route_arrival_time = request.POST.get('route_arrival_time')
            route_duration = request.POST.get('route_duration')  
            
            print(f"route_name: {route_name}, route_number: {route_number}, route_source_code: {route_source_code}, route_destination_code: {route_destination_code}")
            print(f"route_base_fare: {route_base_fare}, route_departure_time: {route_departure_time}, route_arrival_time: {route_arrival_time}, route_duration: {route_duration}")

            try:

                route_source = Station.objects.get(code=route_source_code)
                route_destination = Station.objects.get(code=route_destination_code)
                print(f"route_source: {route_source}, route_destination: {route_destination}")
                
                route = Route.objects.create(
                    name=route_name,
                    number=route_number,
                    source=route_source,
                    destination=route_destination,
                    base_fare=route_base_fare,
                    departure_time=route_departure_time,
                    arrival_time=route_arrival_time,
                    duration=route_duration
                )

                route.save()
                print(f"Route {route_name} created successfully")
                messages.success(request, f"Route {route_name} created successfully")
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes})
            
            except Station.DoesNotExist:
                
                print("One or both stations not found")
                messages.warning(request, 'One or both stations not found.')
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes})
            except Exception as e:
                
                print(f"An error occurred: {str(e)}")
                messages.warning(request, f'An error occurred: {str(e)}')
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes})

        if "add_halt" in request.POST:
            print("Received POST request for add_halt")
            halt_route = request.POST.get('halt_on_route')
            halt_station = request.POST.get('halt_station')
            halt_arrival_time = request.POST.get('halt_arrival_time')
            halt_departure_time = request.POST.get('halt_departure_time')
            halt_order = request.POST.get('halt_order')
            print(f"halt_route: {halt_route}, halt_station: {halt_station}, halt_arrival_time: {halt_arrival_time}, halt_departure_time: {halt_departure_time}, halt_order: {halt_order}")

            try:
                route = Route.objects.get(number=halt_route)
                station = Station.objects.get(code=halt_station)
                print(f"route: {route}, station: {station}")

                halt = HaltStation.objects.create(
                    route=route,
                    station=station,
                    arrival_time=halt_arrival_time,
                    departure_time=halt_departure_time,
                    order=halt_order
                )
                halt.save()
                print(f"Halt station {station} for route {route} added successfully")
                messages.success(request, f"Halt station {station} for route {route} added successfully")
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes})

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                messages.warning(request, f'An error occurred: {str(e)}')
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes})


    print("Received GET request")
    context = {
        'stations': stations,  
        'routes': routes
    }
    return render(request, "dashboard/add_train.html", context)