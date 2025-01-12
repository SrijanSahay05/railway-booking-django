from django.shortcuts import render
from .models import Route, Station, HaltStation, RouteHaltSegments, TrainSegment, Train
from dashboard.models import Day, UpcomingDate
from datetime import timedelta
from django.contrib import messages


def AddTrain(request):
    stations = Station.objects.all()
    routes = Route.objects.all()
    days = Day.objects.all()
    if request.method == "POST":
        #adding a new train route
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
            route_running_days = request.POST.getlist('route_running_days')
            
            print(f"route_name: {route_name}, route_number: {route_number}, route_source_code: {route_source_code}, route_destination_code: {route_destination_code}")
            print(f"route_base_fare: {route_base_fare}, route_departure_time: {route_departure_time}, route_arrival_time: {route_arrival_time}, route_duration: {route_duration}, route_running_days: {route_running_days}", )

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
                for day in route_running_days:
                    running_day = Day.objects.get(code=day)
                    route.running_days.add(running_day)
                    print(f"Added running day {running_day} to route {route}")

                route.save()
                print(f"Route {route_name} created successfully")
                messages.success(request, f"Route {route_name} created successfully")
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes, 'days': days})
            
            except Station.DoesNotExist:
                print("One or both stations not found")
                messages.warning(request, 'One or both stations not found.')
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes, 'days': days})
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                messages.warning(request, f'An error occurred: {str(e)}')
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes, 'days': days})
        
        #adding halt station for a route
        #if "add_halt" in request.POST:
            print("Received POST request for add_halt")
            halt_route = request.POST.get('halt_on_route')
            halt_station = request.POST.get('halt_station')
            halt_arrival_time = request.POST.get('halt_arrival_time')
            halt_departure_time = request.POST.get('halt_departure_time')
            halt_order = request.POST.get('halt_order')
            print(f"halt_route: {halt_route}, halt_station: {halt_station}, halt_arrival_time: {halt_arrival_time}, halt_departure_time: {halt_departure_time}, halt_order: {halt_order}")

            RouteHaltSegments.objects.all().delete()
            print(f"RouteHaltSegments deleted successfully") 
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
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes, 'days': days})

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                messages.warning(request, f'An error occurred: {str(e)}')
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes, 'days': days})

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

                # Add the new halt
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

                # Delete existing halt segments for this route
                RouteHaltSegments.objects.filter(route=route).delete()
                print(f"Deleted existing halt segments for route {route}")

                # Generate new halt segments
                halts = HaltStation.objects.filter(route=route).order_by('order')
                print(f"Number of halts: {halts.count()}")
                if not halts.exists():
                    # If no halts exist, create a single segment from source to destination
                    route_segment = RouteHaltSegments.objects.create(
                        route=route,
                        current_halt=route.destination,
                        previous_halt=route.source,
                        segment_number=1
                    )
                    route_segment.save()
                    print(f"Route segment {route_segment} created for route with no halts")
                else:
                    # Create halt segments for each halt
                    for halt in halts:
                        if halt.order == 1:
                            previous_halt = halt.route.source
                        else:
                            previous_halt = halts.get(order=halt.order - 1).station

                        route_segment = RouteHaltSegments.objects.create(
                            route=route,
                            current_halt=halt.station,
                            previous_halt=previous_halt,
                            segment_number=halt.order
                        )
                        route_segment.save()
                        print(f"Route segment {route_segment} created successfully")

                    # Add the final segment to the destination
                    last_halt = halts.last()
                    route_segment = RouteHaltSegments.objects.create(
                        route=route,
                        current_halt=route.destination,
                        previous_halt=last_halt.station,
                        segment_number=last_halt.order + 1
                    )
                    route_segment.save()
                    print(f"Final route segment {route_segment} created successfully")

                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes, 'days': days})
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                messages.warning(request, f'An error occurred: {str(e)}')
                return render(request, "dashboard/add_train.html", {'stations': stations, 'routes': routes, 'days': days})


    print("Received GET request")
    context = {
        'stations': stations,  
        'routes': routes,
        'days': days,
    }
    
    # making routesegments using available trains and halts
    try:
        routes = Route.objects.all()
        for route in routes:
            halts = HaltStation.objects.all().filter(route=route).order_by('order')
            if not halts.exists():
                route_segment = RouteHaltSegments.objects.create(
                    route=route,
                    current_halt=route.destination,
                    previous_halt=route.source,
                    segment_number=1
                )
                route_segment.save()
                print(f"Route segment {route_segment} created for route with no halts")
            for halt in halts:
                
                if halt.order == 1:
                    previous_halt = halt.route.source
                else:
                    previous_halt = halts.get(order=halt.order-1).station
                if not RouteHaltSegments.objects.filter(route=route, current_halt=halt.station, previous_halt=previous_halt, segment_number=halt.order).exists():
                    route_segment = RouteHaltSegments.objects.create(
                        route=route,
                        current_halt=halt.station,
                        previous_halt=previous_halt,
                        segment_number=halt.order
                    )
                    route_segment.save()
                    print(f"Route segment {route_segment} created successfully")
            if halt.order == len(halts):
                if not RouteHaltSegments.objects.filter(route=route, current_halt=route.destination, previous_halt=halts.get(order=halt.order).station, segment_number=halt.order+1).exists():
                    route_segment = RouteHaltSegments.objects.create(
                        route=route,
                        current_halt=route.destination,
                        previous_halt=halts.get(order=halt.order).station,
                        segment_number=halt.order+1
                    )
                    route_segment.save()
                    print(f"Route segment {route_segment} created successfully")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.warning(request, f'An error occurred: {str(e)}')
    
    #making train segments using available route-segments and upcoming dates
    try:
        routes = Route.objects.all()
        dates = UpcomingDate.objects.filter(day__routes__in=routes).distinct()
        for route in routes:
            for date in dates:
                route_segments = RouteHaltSegments.objects.all().filter(route=route).order_by('segment_number')
                for segment in route_segments:
                    if not TrainSegment.objects.filter(halt_segment=segment, date=date).exists():
                        train_segment = TrainSegment.objects.create(
                            halt_segment=segment,
                            date=date
                        )
                        train_segment.save()
                        print(f"Train segment {train_segment} created successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.warning(request, f'An error occurred: {str(e)}')

    #making train using available route for upcoming dates (remove this when switching to halt-segment part)
    try:
        routes = Route.objects.all()
        dates = UpcomingDate.objects.filter(day__routes__in=routes).distinct()
        for rotue in routes:
            for date in dates:
                if not Train.objects.filter(route=route, date=date).exists():
                    train = Train.objects.create(
                        route=route,
                        date=date
                    )
                    train.save()
                    print(f"Train {train} created successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.warning(request, f'An error occurred: {str(e)}')

    
    return render(request, "dashboard/add_train.html", context)


def RouteSegments(request):
    pass