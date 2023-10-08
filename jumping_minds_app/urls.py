from django.urls import path
from . import views

urlpatterns = [
    path('NumberOfElevator',views.Elevators.create_n_elevators,name='get_number_of_elevators'),
    path('AllElevatorInfo',views.Elevators.get_all_elevator_info,name='get_all_elevator_info'),
    path('NextDestination',views.Elevators.next_destination,name='next_destination'),
    path('Direction',views.Elevators.get_direction,name='get_direction'),
    path('History',views.History.get_history,name='get_history'),
    path('UpdateMaintenance',views.Elevators.update_maintenance,name='update_maintenance'),
    path('UpdateDoorState',views.Elevators.update_door,name='update_door'),
    path('AssignElevator',views.Elevators.assign_elevator,name='assign_elevator'),
]
