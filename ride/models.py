from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime

class Vehicle(models.Model):
    type = models.CharField(max_length = 100)
    plate_number = models.CharField(max_length = 10)
    capacity = models.PositiveSmallIntegerField()
    optional = models.CharField(max_length = 200, blank = True)

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    vehicle = models.OneToOneField(Vehicle, on_delete = models.CASCADE)
    lisence = models.CharField(max_length = 100)
    firstName = models.CharField(max_length = 30)
    lastName = models.CharField(max_length = 30)

class Ride(models.Model):
    STATUS = (
        ('OP', 'Open'),
        ('CF', 'Confirmed'),
        ('CP', 'Completed'),
        ('CC', 'Canceled'),
    )
    #TBD: on_delete is related to one-to-many relationship
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete = models.SET_NULL, null = True)
    destination_address = models.CharField(max_length = 200)
    #TBD: to select date instead of typing
    arrival_datetime = models.DateTimeField(null = True)
    sharability = models.BooleanField(default = False)
    passenger_number = models.PositiveSmallIntegerField()
    status = models.CharField(max_length = 2, choices = STATUS, default = "OP")
    optional = models.CharField(max_length = 200, blank = True)
    def __str__(self):
        return self.destination_address
    #TBD: id starts from 3, wtf?    

class ShareRide(models.Model):
    ride = models.ForeignKey(Ride, on_delete = models.CASCADE)
    sharer = models.ForeignKey(User, on_delete = models.CASCADE)

