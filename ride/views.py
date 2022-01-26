from django.shortcuts import render
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
            #owner= request.POST["owner"],
        )
        newRide.save()
        return HttpResponse("Hi, you have passed the OA.")
    else:
        return HttpResponse("The method is not POST!")
