from django.urls import path

from . import views

app_name = 'ride'
urlpatterns = [
    path('requestInfo/', views.requestInfo, name = 'requestInfo'),
    path('requestRide/', views.requestRide, name = 'requestRide'),
    path('viewRides/', views.viewRides, name = 'viewRides'),
    path('<int:ride_id>/viewInfo', views.viewInfo, name = 'viewInfo'),
    
]
