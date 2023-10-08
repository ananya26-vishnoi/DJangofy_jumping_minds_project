from .models import *
from django.http import JsonResponse
from dotenv import load_dotenv 
load_dotenv()
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .tasks import *

class Helper:
    '''
    This class encapsulates all helper functions
    '''
    def assign_elevator_to_floor(floor):
        '''
        This function is used to assign most optimal elevator to a floor basd on instantaneous data

        Parameters:
        floor (int): The floor to which the elevator is to be assigned

        Returns:
        Elevator: The elevator object which is assigned to the floor. It will be None if no elevator is available
        '''
        available_elevators = Elevator.objects.filter(maintaintenance=False, is_running=True)

        if not available_elevators:
            # No available elevators
            return None

        # Calculate the estimated arrival time for each elevator
        best_elevator = None
        min_arrival_time = float('inf')  # Initialize with positive infinity

        for elevator in available_elevators:
            if elevator.current_floor == floor:
                # If the elevator is already at the requested floor, return it immediately
                return elevator

            if elevator.direction == "stable" or elevator.direction == "up":
                # Elevator is either stable or moving up
                if elevator.current_floor < floor:
                    # Elevator is below the requested floor and moving up, calculate arrival time
                    arrival_time = abs(elevator.current_floor - floor)
                    if arrival_time < min_arrival_time:
                        best_elevator = elevator
                        min_arrival_time = arrival_time

            if elevator.direction == "stable" or elevator.direction == "down":
                # Elevator is either stable or moving down
                if elevator.current_floor > floor:
                    # Elevator is above the requested floor and moving down, calculate arrival time
                    arrival_time = abs(elevator.current_floor - floor)
                    if arrival_time < min_arrival_time:
                        best_elevator = elevator
                        min_arrival_time = arrival_time

        if best_elevator:
            return best_elevator
        else:
            # No suitable elevator found
            return None

class Elevators:
    '''
    This class encapsulates all elevator related functions
    '''
    @api_view(['POST'])
    def create_n_elevators(request):
        '''
        This function is used to create n elevators

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''

        # Check if number_of_elevators is present in request. If not, return error
        if "number_of_elevators" not in request.data:
            return Response({"error":"Number of Elevator not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Create n elevators
        number_of_elevators = request.data['number_of_elevators']
        for i in range(number_of_elevators):
            elevator = Elevator.objects.create()
            elevator.save()
            history=History.objects.create(elevator_id=elevator,log="Elevator id "+str(elevator.id)+" created" )
            history.save()
        
        # Return success
        return Response({"success":"Elevator created"},status=status.HTTP_200_OK)

    @api_view(['GET'])
    def get_all_elevator_info(request):
        '''
        This function is used to get all elevator info

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''

        # Get all elevators and serialize them
        elevators = Elevator.objects.all()
        serializer = ElevatorSerializer(elevators, many=True)

        # Return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def next_destination(request):
        '''
        This function is used to get next destination of elevator

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''

        # Check if elevator_id is present in request. If not, return error
        if "elevator_id" not in request.data:
            return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Get elevator
        elevator_id = request.data['elevator_id']
        elevator = Elevator.objects.get(id=elevator_id)

        # Check if elevator is running. If not, return error
        if elevator.is_running == False:
            return Response({"error":"Elevator is not running"},status=status.HTTP_400_BAD_REQUEST)
        
        # Check if elevator is under maintenance. If yes, return error
        if elevator.maintaintenance == True:
            return Response({"error":"Elevator is under maintenance"},status=status.HTTP_400_BAD_REQUEST)
        
        # Return next destination
        next_destination_floor = elevator.destination_floor[0] if elevator.destination_floor else None
        return JsonResponse({'next_destination_floor': next_destination_floor},status=status.HTTP_200_OK)
        
    @api_view(['GET'])
    def get_direction(request):
        '''
        This function is used to get direction of elevator

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''
        # Check if elevator_id is present in request. If not, return error
        if "elevator_id" not in request.data:
            return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Get elevator
        elevator_id = request.data['elevator_id']
        elevator = Elevator.objects.get(id=elevator_id)

        # Check if elevator is running. If not, return error
        if elevator.is_running == False:
            return Response({"error":"Elevator is not running"},status=status.HTTP_400_BAD_REQUEST)
        
        # Check if elevator is under maintenance. If yes, return error
        if elevator.maintaintenance == True:
            return Response({"error":"Elevator is under maintenance"},status=status.HTTP_400_BAD_REQUEST)
        
        # Return direction
        return JsonResponse({'direction': elevator.direction},status=status.HTTP_200_OK)

    @api_view(['PUT'])
    def update_maintenance(request):
        '''
        This function is used to update maintenance state of elevator

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''
        # Check if elevator_id is present in request. If not, return error
        if "elevator_id" not in request.data:
            return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Get elevator
        elevator_id = request.data['elevator_id']
        elevator = Elevator.objects.get(id=elevator_id)

        # Check if elevator is running. If not, return error
        if "maintenance_state" not in request.data:
            return Response({"error":"Maintenance State not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Update maintenance state
        maintenance_state = request.data['maintenance_state']
        elevator.maintaintenance = maintenance_state
        elevator.is_running = False
        elevator.save()
        history=History.objects.create(elevator_id=elevator,log="Elevator id "+str(elevator.id)+" is under maintenance" )
        history.save()

        # Return success based on maintenance state
        if maintenance_state==False:
            return Response({"success":"Elevator is not under maintenance"},status=status.HTTP_200_OK)
        return Response({"success":"Elevator is under maintenance"},status=status.HTTP_200_OK)

    @api_view(['PUT'])
    def update_door(request):
        '''
        This function is used to update door state of elevator

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''
        # Check if elevator_id is present in request. If not, return error
        if "elevator_id" not in request.data:
            return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Check if door_state is present in request. If not, return error
        if "door_state" not in request.data:
            return Response({"error":"Door State not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Get data from request and update door state
        door_state = request.data['door_state']
        elevator_id = request.data['elevator_id']
        elevator = Elevator.objects.get(id=elevator_id)
        elevator.door_state = door_state
        elevator.save()

        # Update history
        history=History.objects.create(elevator_id=elevator,log="Elevator id "+str(elevator.id)+" door closed" )
        history.save()

        # Return success based on door state
        if door_state==True:
            elevator.is_running=True
            elevator.save()
            return Response({"success":"Elevator door open"},status=status.HTTP_200_OK)
        return Response({"success":"Elevator door closed"},status=status.HTTP_200_OK)

    
    @api_view(['PUT'])
    def assign_elevator(request):
        '''
        This function is used to assign elevator to a floor

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''

        # Check if floor is present in request. If not, return error
        if "floor" not in request.data:
            return Response({"error":"Floor not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Get floor and assign elevator to it
        floor = request.data['floor']
        optimal_elevator=Helper.assign_elevator_to_floor(floor)
        update_elevator_state.delay(optimal_elevator.id,floor)

        # Return success
        return Response({"success":"Elevator assigned","elevator_id":optimal_elevator.id},status=status.HTTP_200_OK)

class HistoryFunction:

    @api_view(['GET'])
    def get_history(request):
        '''
        This function is used to get history of elevator

        Parameters:
        request (Request): The request object

        Returns:
        Response: The response object
        '''

        # Check if elevator_id is present in request. If not, return error
        if "elevator_id" not in request.data:
            return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        # Get history and serialize it
        elevator_id = request.data['elevator_id']
        history = History.objects.filter(elevator_id=elevator_id)
        serializer = HistorySerializer(history, many=True)

        # Return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
