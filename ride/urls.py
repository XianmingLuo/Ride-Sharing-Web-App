from django.urls import path

from . import views

app_name = 'ride'
urlpatterns = [
    path('requestInfo/', views.requestInfo, name = 'requestInfo'),
    path('requestRide/', views.requestRide, name = 'requestRide'),
    path('owner/viewRides/', views.viewOwnerRides, name = 'viewOwnerRides'),
    path('driver/viewRides/', views.viewDriverRides, name = 'viewDriverRides'),
    path('sharer/viewRides/', views.viewSharerRides, name = 'viewSharerRides'),
    path('driverInfo/', views.driverInfo, name = 'driverInfo'),
    path('driverReg/', views.driverReg, name = 'driverReg'),
    path('searchRides/', views.searchRides, name = 'searchRides'),
    path('selectRole/', views.selectRole, name = 'selectRole'),
    path('<int:ride_id>/viewInfo', views.viewInfo, name = 'viewInfo'),
]
