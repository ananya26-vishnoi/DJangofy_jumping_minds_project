from celery import shared_task
from .models import Elevator

@shared_task
def update_elevator_state(optimal_elevator_id,floor):
    elevator = Elevator.objects.get(id=optimal_elevator_id)
    temporary_destination_floor=elevator.destination_floor
    

    temporary_destination_floor.append(floor)
    sorted_list = sorted(temporary_destination_floor)
    elevator.destination_floor = sorted_list
    

    latest_destination_floor = elevator.destination_floor[0]
    if latest_destination_floor > elevator.current_floor:
        elevator.direction = "up"
    elif latest_destination_floor < elevator.current_floor:
        elevator.direction = "down"
    else:
        elevator.direction = "stable"


    if latest_destination_floor==elevator.current_floor:
        elevator.is_running=False 
    
    if elevator.is_running==True:
        elevator.current_floor=elevator.current_floor+1 if elevator.direction=="up" else elevator.current_floor-1