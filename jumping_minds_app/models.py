from django.db import models 
class Elevator(models.Model):
    direction = models.CharField(max_length=1000)
    current_floor = models.IntegerField(default=0)
    destination_floor = models.CharField(max_length=1000)
    maintamaintenance = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    door_state = models.BooleanField(default=False)
class History(models.Model):
    elevator_id = models.ForeignKey(on_delete=models.CASCADE)
    log = models.CharField(max_length=1000)
     = models.CharField(max_length=1000)
