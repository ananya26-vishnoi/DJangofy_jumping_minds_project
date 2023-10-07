from django.db import models 
from django.contrib.postgres.fields import JSONField

class Elevator(models.Model):
    direction = models.CharField(default="stable", max_length=1000)
    current_floor = models.IntegerField(default=0)
    destination_floor = models.JSONField(default=[])
    maintaintenance = models.BooleanField(default=False)
    is_running = models.BooleanField(default=True)
    door_state = models.BooleanField(default=False) # False for closed and True for open

class History(models.Model):
    elevator_id = models.ForeignKey(Elevator,on_delete=models.CASCADE)
    log = models.CharField(max_length=1000)