from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ride, Driver, Vehicle, ShareRide
# Create your views here.
def requestInfo(request):
    return render(request, 'ride/requestInfo.html')
def shareInfo(request):
    return render(request, 'ride/shareInfo.html')

def requestRide(request):
    if request.method == 'POST':
        newRide = Ride.objects.create(
            destination_address = request.POST["destination_address"],
            arrival_datetime = request.POST["arrival_datetime"],
            passenger_number= request.POST["passenger_number"],
            sharability= request.POST["sharability"],
            owner= request.user,
        )
        newRide.save()
        return redirect('home')
    else:
        return HttpResponse("The method is not POST!")
def matchRides(request):
    if request.method == 'POST':
        print("Hi im trying to join a ride!")
        sharableRides = Ride.objects.filter(sharability = True).exclude(owner = request.user)
        destMatchedRides = sharableRides.filter(destination_address = request.POST["destination_address"])
        timeMatchedRides = destMatchedRides.filter(arrival_datetime__range = (request.POST['arrival_datetime_start'], request.POST['arrival_datetime_end']))
    return render(request, 'ride/matchedRides.html', {'rides': timeMatchedRides})
def viewRides(request, role):
    if request.method == 'GET':
        if role == 'driver':
            rides = Ride.objects.filter(driver_id = request.user.id)
        elif role == 'owner':
            rides = Ride.objects.filter(owner = request.user)
        elif role == 'sharer':
            rides = Ride.objects.filter()
            pass
            rides = Ride.objects.filter()
        else:
            pass
            #TBD 404
        return render(request, 'ride/viewRides.html', {'rides': rides})
    
def viewInfo(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo_base.html', {'ride': ride})
def driverInfo(request):
    return render(request, 'ride/driverInfo.html')
def driverReg(request):
    if request.method == 'POST':
        newVehicle = Vehicle.objects.create(
            type = request.POST["vehicle_type"],
            plate_number = request.POST["plate_number"],
            capacity = request.POST["vehicle_capacity"],
        )
        newVehicle.save()
        newDriver = Driver.objects.create(
            user = request.user,
            vehicle = newVehicle,
            lisence = request.POST["driver_lisence"],
        )
        newDriver.save()
        return redirect('home')

def searchRides(request):
    try:
        driver = Driver.objects.get(user = request.user)
    except Driver.DoesNotExist:
        return HttpResponse("You are not a driver")
    else:
        vehicle = Vehicle.objects.get(pk = driver.vehicle_id)
        openRides = Ride.objects.filter(is_complete = False).filter(driver__isnull = True).exclude(owner = request.user)
        capMatchedRides = openRides.filter(passenger_number__lte = vehicle.capacity)
        return render(request, 'ride/searchRides.html', {'rides': capMatchedRides})

def selectRole(request):
    return render(request, 'ride/selectRole.html')
def confirmRide(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    ride.driver = Driver.objects.get(pk = request.user.id)
    ride.save()
    print(ride.driver)
    print(ride)
    return redirect('ride:searchRides')
def joinRide(request, ride_id):
    rideToJoin = Ride.objects.get(pk = ride_id)
    ShareRide.objects.create(
        ride = rideToJoin,
        sharer = request.user
    )
    return redirect('home')

def confirmInfo(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo_driver.html', {'ride': ride})
def matchedInfo(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo_sharer.html', {'ride': ride})

def editInfo(request):
    return render(request, 'ride/editInfo.html')
def submitDriverEdition(request):
    try:
        driver = Driver.objects.get(pk = request.user.id)
        vehicle = driver.vehicle
    except Driver.DoesNotExist:
        return HttpResponse("You have not registered as a driver")
    else:
        if request.method == 'POST':
            driver.lisence = request.POST['driver_lisence']
            vehicle.type = request.POST['vehicle_type']
            vehicle.plate_number = request.POST['plate_number']
            vehicle.capacity = request.POST['vehicle_capacity']
            vehicle.save()
            driver.save()
        return redirect('ride:editInfo')

def editRides(request):
    rides = Ride.objects.filter(owner = request.user)
    return render(request, 'ride/editRides.html', {'rides': rides})

def editSelectedRide(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/editSelectedRide.html', {'ride': ride})


def editDriverInfo(request):
    if request.method == 'GET':
        driver = Driver.objects.get(user = request.user)
        return render(request, 'ride/editDriverInfo.html', {'driver': driver})

        


