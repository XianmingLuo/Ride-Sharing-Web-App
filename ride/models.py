from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ride(models.Model):
    #TBD: on_delete is related to many-to-one relationship
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    destination_address = models.CharField(max_length = 200)
    #TBD: to select date instead of typing
    arrival_time = models.DateTimeField('arrival time')
    sharability = models.BooleanField(default = False)
    passenger_number = models.PositiveSmallIntegerField()
    status = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.destination_address
    #TBD: id starts from 3, wtf?    


class Vehicle(models.Model):
    type = models.CharField(max_length = 100)
    plate_number = models.CharField(max_length = 10)
    capacity = models.PositiveSmallIntegerField()

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    vehicle = models.OneToOneField(Vehicle, on_delete = models.CASCADE)
    lisence = models.CharField(max_length = 100)
