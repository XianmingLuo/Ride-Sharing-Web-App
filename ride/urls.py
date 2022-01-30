from django.urls import path

from . import views

app_name = 'ride'
urlpatterns = [
    path('requestInfo/', views.requestInfo, name = 'requestInfo'),
    path('requestRide/', views.requestRide, name = 'requestRide'),
    path('shareInfo/', views.shareInfo, name = 'shareInfo'),
    path('matchRides/', views.matchRides, name = 'matchRides'),
    path('<str:role>/viewRides/', views.viewRides, name = 'viewRides'),
    path('driverInfo/', views.driverInfo, name = 'driverInfo'),
    path('driverReg/', views.driverReg, name = 'driverReg'),
    path('searchRides/', views.searchRides, name = 'searchRides'),
    path('selectRole/', views.selectRole, name = 'selectRole'),
    path('<int:ride_id>/viewInfo', views.viewInfo, name = 'viewInfo'),
    path('<int:ride_id>/confirmRide', views.confirmRide, name = 'confirmRide'),
    path('<int:ride_id>/confirmInfo', views.confirmInfo, name = 'confirmInfo'),
    path('<int:ride_id>/matchedInfo', views.matchedInfo, name = 'matchedInfo'),
    path('<int:ride_id>/joinRide', views.joinRide, name = 'joinRide'),
    path('editInfo/', views.editInfo, name = 'editInfo'),
    path('editRides/', views.editRides, name = 'editRides'),
    path('<int:ride_id>/editRide/', views.editRide, name = 'editRide'),
    path('editDriverInfo/', views.editDriverInfo, name = 'editDriverInfo'),
    path('submitDriverEdition/', views.submitDriverEdition, name = 'submitDriverEdition'),
    path('<int:ride_id>/submitRideEdition/', views.submitRideEdition, name = 'submitRideEdition'),
    path('<int:ride_id>/completeRide', views.completeRide, name = 'completeRide'),
    path('<int:ride_id>/cancelRide', views.cancelRide, name = 'cancelRide'),
    
]
