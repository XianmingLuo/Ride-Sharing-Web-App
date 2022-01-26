from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ride
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
    print(ride)
    print(ride.destination_address)
    return render(request, 'ride/viewInfo.html', {'ride': ride})
