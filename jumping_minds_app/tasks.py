from celery import shared_task
from .models import Elevator
import time
import threading  

# Create a dictionary to hold locks for each elevator
elevator_locks = {}

@shared_task
def update_elevator_state(elevator_id,floor):
    # Getting elevator object
    elevator = Elevator.objects.get(id=elevator_id)

    # Creating a temporary list to store the previous destination floors
    temporary_destination_floor=elevator.destination_floor
    
    # Adding new floor and sorting list
    temporary_destination_floor.append(floor)
    sorted_list = sorted(temporary_destination_floor)
    elevator.destination_floor = sorted_list
    elevator.save()
    print("destination floor updated to "+str(elevator.destination_floor))

    # Making sure some other threading loop is not already running. Using semaphore
    with elevator_locks.setdefault(elevator_id, threading.Lock()):
        elevator = Elevator.objects.get(id=elevator_id)

        # Getting nest floor elevator has to go on
        latest_destination_floor = elevator.destination_floor[0]

        # Setting direction
        if latest_destination_floor > elevator.current_floor:
            elevator.direction = "up"
        elif latest_destination_floor < elevator.current_floor:
            elevator.direction = "down"
        else:
            elevator.direction = "stable"
        elevator.save()
        print("direction updated to "+str(elevator.direction))

        # Checking if elevator has reached the destination floor thus stopping elevator from moving
        if latest_destination_floor==elevator.current_floor:
            elevator.destination_floor.remove(elevator.current_floor)
            elevator.is_running=False 
            elevator.save()
            print("Elevator has reached to the destination floor and is waiting for doors to open"+str(elevator.is_running))
        
        # Getting last floor where elevator has to go to 
        final_floor = elevator.destination_floor[len(elevator.destination_floor)-1]
        while elevator.current_floor != final_floor:
            if elevator.is_running==True:
                elevator.current_floor=elevator.current_floor+1 if elevator.direction=="up" else elevator.current_floor-1
            elevator.save()
            print("Elevator is moving to the destination floor "+str(elevator.current_floor))

            # sleeping for 30 seconds - denotes going from one floor to another floor
            time.sleep(30)

        # Setting elevator to stable once it has reached the final floor
        elevator.direction="stable"
        elevator.save()
        print("Elevator is stable now"+str(elevator.direction))

    # Removing lock from dictionary once elevator has reached the final floor
    del elevator_locks[elevator_id]