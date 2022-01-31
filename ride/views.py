from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.mail import send_mail
from .models import Ride, Driver, Vehicle, ShareRide
from django.contrib.auth.models import User
# Create your views here.
def requestInfo(request):
    return render(request, 'ride/requestInfo.html', {'vehicle_types': Vehicle.TYPES})
def shareInfo(request):
    return render(request, 'ride/shareInfo.html')

def requestRide(request):
    if request.method == 'POST':
        newRide = Ride.objects.create(
            destination_address = request.POST["destination_address"],
            arrival_datetime = request.POST["arrival_datetime"],
            passenger_number= eval(request.POST["passenger_number"]),
            sharability= request.POST["sharability"],
            owner= request.user,
            status = "OP",
            type = request.POST["vehicle_type"],
            optional = request.POST["optional"],
        )
        newRide.save()
        return redirect('home')
    else:
        return HttpResponse("The method is not POST!")
#This view is used to search for open, sharable rides according to sharers' destination, arrival time window, and number of passengers?
def matchRides(request):
    if request.method == 'POST':
        sharableRides = Ride.objects.filter(status = "OP").filter(sharability = True).exclude(owner = request.user)#.exclude(ride.shareride_set.get(sharer = request.user))
        destMatchedRides = sharableRides.filter(destination_address = request.POST["destination_address"])
        timeMatchedRides = destMatchedRides.filter(arrival_datetime__range = (request.POST['arrival_datetime_start'], request.POST['arrival_datetime_end']))
        
        request.session['passenger_number'] = eval(request.POST['passenger_number'])
    return render(request, 'ride/matchedRides.html', {'rides': timeMatchedRides})

def viewRides(request, role):
    if request.method == 'GET':
        if role == 'driver':
            rides = Ride.objects.filter(driver_id = request.user.id)
            template = "ride/viewRides_driver.html"
        elif role == 'owner':
            rides = Ride.objects.filter(owner = request.user)
            template = "ride/viewRides_owner.html"
        elif role == 'sharer':
            rides = Ride.objects.filter(shareride__sharer = request.user)
            template = "ride/viewRides_sharer.html"
        else:
            pass
            #TBD 404
        return render(request, template , {'rides': rides})
    
def rideDetail(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo_base.html', {'ride': ride})
def driverInfo(request):
    return render(request, 'ride/driverInfo.html', {'vehicle_types': Vehicle.TYPES})
def driverReg(request):
    if request.method == 'POST':
        newVehicle = Vehicle.objects.create(
            type = request.POST["vehicle_type"],
            plate_number = request.POST["plate_number"],
            capacity = eval(request.POST["vehicle_capacity"]),
            specialInfo = request.POST["vehicle_specialInfo"],
        )
        newVehicle.save()
        newDriver = Driver.objects.create(
            user = request.user,
            vehicle = newVehicle,
            license= request.POST["driver_license"],
            firstName = request.POST["firstName"],
            lastName = request.POST["lastName"],
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
        openRides = Ride.objects.filter(status = "OP").exclude(owner = request.user)
        typeMatchedRides = openRides.filter(Q(type = "")|Q(type = vehicle.type))
        specialMatchedRides = typeMatchedRides.filter(Q(optional = "")|Q(optional = vehicle.specialInfo))
        capMatchedRides = specialMatchedRides.filter(passenger_number__lte = vehicle.capacity)
        return render(request, 'ride/viewRides_search.html', {'rides': capMatchedRides})

def selectRole(request):
    return render(request, 'ride/selectRole.html')
def confirmRide(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    ride.driver = Driver.objects.get(pk = request.user.id)
    ride.status = "CF"
    mailSubject = "Your ride to " + ride.destination_address + " at " + ride.arrival_datetime.strftime("%m/%d/%Y, %H:%M:%S") + " has been confirmed!"
    mailMessage = ride.driver.description() + ride.driver.vehicle.description()
    sharers = User.objects.all().filter(shareride__ride = ride)
    recipient_emails = [ride.owner.email]
    for sharer in sharers:
        recipient_emails.append(sharer.email)
    send_mail(
        mailSubject,
        mailMessage,
        from_email = None,
        recipient_list = recipient_emails,
        fail_silently = False,
        )
    ride.save()
    return redirect('ride:searchRides')
def joinRide(request, ride_id):
    rideToJoin = Ride.objects.get(pk = ride_id)
    rideToJoin.passenger_number += request.session["passenger_number"]
    ShareRide.objects.create(
        sharer = request.user,
        passenger_number = request.session["passenger_number"],
        ride = rideToJoin,
        )
    request.session["passenger_number"] = -1
    rideToJoin.save()
    return redirect('home')
def cancelShare(request, ride_id):
    rideToQuit = Ride.objects.get(pk = ride_id)
    shareToDelete = ShareRide.objects.get(Q(ride = rideToQuit) & Q(sharer = request.user))
    shareToDelete.delete()
    return redirect('/ride/sharer/viewRides')
def confirmInfo(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo_driver.html', {'ride': ride})
def matchedInfo(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/viewInfo_sharer.html', {'ride': ride})

def submitDriverEdition(request):
    try:
        driver = Driver.objects.get(pk = request.user.id)
        vehicle = driver.vehicle
    except Driver.DoesNotExist:
        return HttpResponse("You have not registered as a driver")
    else:
        if request.method == 'POST':
            driver.firstName = request.POST['firstName']
            driver.lastName = request.POST['lastName']
            driver.license = request.POST['driver_license']
            vehicle.type = request.POST['vehicle_type']
            vehicle.plate_number = request.POST['plate_number']
            vehicle.capacity = request.POST['vehicle_capacity']
            vehicle.specialInfo = request.POST['vehicle_specialInfo']
            vehicle.save()
            driver.save()
        return redirect('home')
def submitRideEdition(request, ride_id):
    editedRide = get_object_or_404(Ride, pk = ride_id)
    if request.method == 'POST':
        editedRide.destination_address = request.POST["destination_address"]
        editedRide.arrival_datetime = request.POST["arrival_datetime"]
        editedRide.passenger_number= request.POST["passenger_number"]
        editedRide.type = request.POST["vehicle_type"]
        editedRide.sharability= request.POST["sharability"]
        editedRide.optional = request.POST["optional"]
        editedRide.save()
    return redirect('home')
        
def editRides(request):
    editableRides = Ride.objects.filter(owner = request.user).filter(status = "OP")
    return render(request, 'ride/editRides.html', {'rides': editableRides})

def editRide(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    return render(request, 'ride/editRide.html', {'ride': ride, 'vehicle_types': Vehicle.TYPES})
def cancelRide(request, ride_id):
    ride = get_object_or_404(Ride, pk = ride_id)
    ride.status = "CC"
    ride.save()
    return redirect('home')

def editDriverInfo(request):
    if request.method == 'GET':
        driver = Driver.objects.get(user = request.user)
        return render(request, 'ride/editDriverInfo.html', {'driver': driver})
def completeRide(request, ride_id):
    completedRide = Ride.objects.get(pk = ride_id)
    completedRide.status = "CP"
    completedRide.save()
    return redirect('/ride/driver/viewRides')
        


