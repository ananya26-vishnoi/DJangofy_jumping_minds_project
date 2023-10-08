from django.urls import path
from . import views

urlpatterns = [
    path('NumberOfElevator',views.get_number_of_elevators,name='get_number_of_elevators'),
    path('AllElevatorInfo',views.get_all_elevator_info,name='get_all_elevator_info'),
    path('NextDestination',views.next_destination,name='next_destination'),
    path('Direction',views.get_direction,name='get_direction'),
    path('History',views.get_history,name='get_history'),
    path('UpdateMaintenance',views.update_maintenance,name='update_maintenance'),
    path('UpdateDoorState',views.update_door,name='update_door'),
    path('AssignElevator',views.assign_elevator,name='assign_elevator'),
]
