from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ride, Driver, Vehicle
# Create your views here.
def requestInfo(request):
    return render(request, 'ride/requestInfo.html')
def requestRide(request):
    if request.method == 'POST':
        newRide = Ride.objects.create(
            destination_address = request.POST["destination_address"],
            arrival_date = request.POST["arrival_date"],
            arrival_time = request.POST["arrival_time"],
            passenger_number= request.POST["passenger_number"],
            sharability= request.POST["sharability"],
            owner= request.user,
        )
        newRide.save()
        return redirect('home')
    else:
        return HttpResponse("The method is not POST!")

def viewRides(request, role):
    if request.method == 'GET':
        if role == 'driver':
            rides = Ride.objects.filter(driver_id = request.user.id)
        elif role == 'owner':
            rides = Ride.objects.filter(owner = request.user)
        elif role == 'sharer':
            pass
        else:
            pass
            #TBD 404
        return render(request, 'ride/viewRides.html', {'rides': rides})
    
def viewInfo(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo_driver.html', {'ride': ride})
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
    driver = Driver.objects.filter(user_id = request.user.id)
    openRides = Ride.objects.filter(is_complete = False).filter(driver__isnull = True)
    if bool(driver) == False:
        return HttpResponse("You are not a driver")
    else:
        return render(request, 'ride/viewRides.html', {'rides': openRides})

def selectRole(request):
    return render(request, 'ride/selectRole.html')
def confirmRide(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    ride.driver = Driver.objects.get(pk = request.user.id)
    ride.save()
    print(ride.driver)
    print(ride)
    return redirect('ride:searchRides')
    
    



        
        
