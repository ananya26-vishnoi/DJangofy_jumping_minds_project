from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from dotenv import load_dotenv 
load_dotenv()
import json
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .tasks import *


@api_view(['POST'])
def get_number_of_elevators(request):
    if "number_of_elevators" not in request.data:
        return Response({"error":"Number of Elevator not Found"},status=status.HTTP_400_BAD_REQUEST)
    
    number_of_elevators = request.data['number_of_elevators']
    for i in range(number_of_elevators):
        elevator = Elevator.objects.create()
        elevator.save()
        history=History.objects.create(elevator_id=elevator,log="Elevator id "+str(elevator.id)+" created" )
        history.save()
    return Response({"success":"Elevator created"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_elevator_info(request):
    elevators = Elevator.objects.all()
    serializer = ElevatorSerializer(elevators, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def next_destination(request):
    if "elevator_id" not in request.data:
        return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
    elevator_id = request.data['elevator_id']
    elevator = Elevator.objects.get(id=elevator_id)
    if elevator.is_running == False:
        return Response({"error":"Elevator is not running"},status=status.HTTP_400_BAD_REQUEST)
    if elevator.maintaintenance == True:
        return Response({"error":"Elevator is under maintenance"},status=status.HTTP_400_BAD_REQUEST)
    next_destination_floor = elevator.destination_floor[0] if elevator.destination_floor else None
    return JsonResponse({'next_destination_floor': next_destination_floor},status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_direction(request):
    if "elevator_id" not in request.data:
        return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
    elevator_id = request.data['elevator_id']
    elevator = Elevator.objects.get(id=elevator_id)
    if elevator.is_running == False:
        return Response({"error":"Elevator is not running"},status=status.HTTP_400_BAD_REQUEST)
    if elevator.maintaintenance == True:
        return Response({"error":"Elevator is under maintenance"},status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'direction': elevator.direction},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_history(request):
    if "elevator_id" not in request.data:
        return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
    elevator_id = request.data['elevator_id']
    history = History.objects.filter(elevator_id=elevator_id)
    serializer = HistorySerializer(history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_maintenance(request):
    if "elevator_id" not in request.data:
        return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
    elevator_id = request.data['elevator_id']
    elevator = Elevator.objects.get(id=elevator_id)
    if "maintenance_state" not in request.data:
        return Response({"error":"Maintenance State not Found"},status=status.HTTP_400_BAD_REQUEST)
    maintenance_state = request.data['maintenance_state']
    elevator.maintaintenance = maintenance_state
    elevator.is_running = False
    elevator.save()
    history=History.objects.create(elevator_id=elevator,log="Elevator id "+str(elevator.id)+" is under maintenance" )
    history.save()
    if maintenance_state==False:
        return 
    return Response({"success":"Elevator is under maintenance"},status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_door(request):
    if "elevator_id" not in request.data:
        return Response({"error":"Elevator ID not Found"},status=status.HTTP_400_BAD_REQUEST)
    if "door_state" not in request.data:
        return Response({"error":"Door State not Found"},status=status.HTTP_400_BAD_REQUEST)
    door_state = request.data['door_state']
    elevator_id = request.data['elevator_id']
    elevator = Elevator.objects.get(id=elevator_id)
    elevator.door_state = door_state
    elevator.save()
    history=History.objects.create(elevator_id=elevator,log="Elevator id "+str(elevator.id)+" door closed" )
    history.save()
    if door_state==True:
        elevator.is_running=True
        elevator.save()
        return Response({"success":"Elevator door open"},status=status.HTTP_200_OK)
    return Response({"success":"Elevator door closed"},status=status.HTTP_200_OK)

def assign_elevator_to_floor(floor):
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

@api_view(['PUT'])
def assign_elevator(request):
    if "floor" not in request.data:
        return Response({"error":"Floor not Found"},status=status.HTTP_400_BAD_REQUEST)
    floor = request.data['floor']
    optimal_elevator=assign_elevator_to_floor(floor)
    update_elevator_state.delay(optimal_elevator.id,floor)
    return Response({"success":"Elevator assigned","elevator_id":optimal_elevator.id},status=status.HTTP_200_OK)


    pass