from django.contrib import admin 
from .models import Elevator
from .models import History

admin.site.register(Elevator)
admin.site.register(History)
