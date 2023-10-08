from rest_framework import serializers 
from .models import Elevator, History

class ElevatorSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Elevator 
        fields = '__all__' 

class HistorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = History 
        fields = '__all__' 
