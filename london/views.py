import time
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Buses
from .services import get_bus


 # 'https://api.tfl.gov.uk/StopPoint/490014050A/arrivals' #Victoria, this is used to second check.
url = 'https://api.tfl.gov.uk/StopPoint/490009333W/arrivals' #Lower Marsh Lane

def index(request):
    """Function to render the index page, this function call the services to get and render the index page"""
    buses = get_bus(url)
    if isinstance(buses, str):
        return HttpResponseNotFound(buses)
    create_bus(buses) #create object after check_error
    refresh_count = buses[0]['timing']['countdownServerAdjustment'] #capture server refresh time
    refresh_count = round(float(refresh_count[6:-5]), 0) #capture seconds for page refresh
    hour = time.strptime(buses[0]['timestamp'][:-3], "%Y-%m-%dT%H:%M:%S.%f")  # Convert to timeformat
    formated_hour = time.strftime("%H:%M:%S", hour)  #get hour to show in index page

    return render(request, 'index.html', {'buses': buses, 'time_now': formated_hour, 'refresh': refresh_count,
                                          'station_name': buses[0]['stationName'] })

def api(request):
    """Function to Call the API of origin"""
    buses = get_bus(url)
    return render(request, 'api.html', {'api': buses})

def results(request):
    '''Function to get all saved data in DB and render the results page'''
    buses = {'bus': list(Buses.objects.all())}
    return render(request, 'results.html', buses)

def create_bus(buses):
    """Function to get data and save to DB"""
    for bus in buses:
        arrival = time.strptime(bus['expectedArrival'], "%Y-%m-%dT%H:%M:%SZ")#Convert to timeformat
        expected = time.strftime("%Y-%m-%d %H:%M", arrival) #get the time in db format
        now = time.strptime(bus['timestamp'][:-2], "%Y-%m-%dT%H:%M:%S.%f")#Convert to timeformat
        time_now = time.strftime("%Y-%m-%d %H:%M", now)#get the time in db format

        try:
            save_bus = Buses.objects.create(line_name= bus['lineName'],
                                            destination_name= bus['destinationName'], vehicle_id= bus['vehicleId'],
                                            expected_arrival=expected, time_now=time_now)
            save_bus.save()
        except:
            pass


