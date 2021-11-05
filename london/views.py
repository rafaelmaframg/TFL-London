import time
from django.db import IntegrityError
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Buses
from .services import get_bus
from django.core.paginator import Paginator, InvalidPage, EmptyPage


# 'https://api.tfl.gov.uk/StopPoint/490014050A/arrivals' #Victoria, this is used to second check.
url = 'https://api.tfl.gov.uk/StopPoint/490009333W/arrivals' #Lower Marsh Lane


def index(request):
    """Function to render the index page, this function call the services to get and render the index page"""
    buses = get_bus(url)
    search = request.GET.get('search')

    if search: #execute the search if the button has clicked
        buses = Buses.objects.all()
        search = request.GET.get('search')
        if search:
            buses = buses.filter(vehicle_id__icontains=search)

            paginator = Paginator(buses, 10)  # paginator for data in results page
            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try:
                bus = paginator.page(page)
            except (EmptyPage, InvalidPage):
                bus = paginator.page(paginator.num_pages)
            return render(request, 'results.html', {'buses': bus})

    if not isinstance(buses, list): #Check Error
        return HttpResponseNotFound(buses)
    create_bus(buses) #Create object
    refresh_count = buses[0]['timing']['countdownServerAdjustment'] #capture server refresh time
    refresh_count = round(float(refresh_count[6:-5]), 0) #capture seconds for page refresh
    hour = time.strptime(buses[0]['timestamp'][:-3], "%Y-%m-%dT%H:%M:%S.%f")  # Convert to timeformat
    formated_hour = time.strftime("%H:%M:%S", hour)  #get hour to show in index page
    return render(request, 'index.html', {'buses': buses, 'time_now': formated_hour,
                                          'refresh': refresh_count, 'station_name': buses[0]['stationName']})


def api(request):
    """Function to Call the API of origin"""
    buses = get_bus(url)
    if not isinstance(buses, list): #Check Error
        return HttpResponseNotFound(buses)
    return render(request, 'api.html', {'api': buses})


def results(request):
    """Function to get all saved data in DB and render the results page"""
    buses = Buses.objects.all()
    search = request.GET.get('search')
    if search:
        buses = buses.filter(vehicle_id__icontains=search)

    paginator = Paginator(buses, 10) #paginator for data in results page
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        bus = paginator.page(page)
    except (EmptyPage, InvalidPage):
        bus = paginator.page(paginator.num_pages)
    return render(request, 'results.html', {'buses': bus})


def create_bus(buses):
    """Function to get data and save to DB"""
    for bus in buses:
        #iterate in each api data and define the variables
        line_name = bus['lineName']
        destination = bus['destinationName']
        vehicle_id = bus['vehicleId']
        arrival = time.strptime(bus['expectedArrival'], "%Y-%m-%dT%H:%M:%SZ")#Convert to timeformat
        expected = time.strftime("%Y-%m-%d %H:%M", arrival) #get the time in db format
        now = time.strptime(bus['timestamp'][:-2], "%Y-%m-%dT%H:%M:%S.%f")#Convert to timeformat
        time_now = time.strftime("%Y-%m-%d %H:%M", now)#get the time in db format

        try:
            #try to create a new object
            save_bus = Buses.objects.create(line_name=line_name,
                                            destination_name=destination, vehicle_id=vehicle_id,
                                            expected_arrival=expected, time_now=time_now)
            save_bus.save()

        except IntegrityError:
            #if object exists, an IntegrityError has returned and this except make an update in DB
            r = Buses.objects.get(vehicle_id=vehicle_id)
            r.line_name = line_name
            r.destination_name = destination
            r.vehicle_id = vehicle_id
            r.expected_arrival = expected
            r.time_now = time_now
            r.save()

