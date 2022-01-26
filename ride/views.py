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
            arrival_time= request.POST["arrival_time"],
            passenger_number= request.POST["passenger_number"],
            sharability= request.POST["sharability"],
            owner= request.user,
            status = 0,
        )
        newRide.save()
        return redirect('home')
    else:
        return HttpResponse("The method is not POST!")
def viewRides(request):
    if request.method == 'GET':
        rides = Ride.objects.filter(owner_id = request.user.id)
        return render(request, 'ride/viewRides.html', {'rides': rides})
def viewInfo(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo.html', {'ride': ride})
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
        
        
