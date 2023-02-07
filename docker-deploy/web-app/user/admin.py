from django.contrib import admin

# Register your models here.

from .models import Driver, User, Ride
from . import models

admin.site.register(Driver)
admin.site.register(Ride)
