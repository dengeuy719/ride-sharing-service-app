from django.db import models
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.postgres.fields import DictionaryField
# Create your models here.

class ThingPriority(models.IntegerChoices):
    Sedan = 4, 'Sedan'
    Coupe = 3, 'Coupe'
    SUV = 5, 'SUV'
    Pickup = 6, 'Pickup'



class Driver(models.Model):
    user = models.OneToOneField(User, related_name='driver2_user_set', on_delete=models.CASCADE)
    vehicle_type = models.IntegerField(verbose_name="Vehicle Type",choices=ThingPriority.choices)
    plate_num = models.CharField(max_length=256,null=True,blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)],null=True,blank=True)
    special_vehicle_info = models.TextField(max_length=256,null=True,blank=True)

class Ride(models.Model):
    id = models.BigAutoField(primary_key=True)
    destination = models.CharField(max_length=256)
    arrival_time = models.DateTimeField(default=timezone.now)
    passenger_number = models.IntegerField(validators=[
            MinValueValidator(1)
        ])
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner_user_set',blank=True,null=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True,related_name='driver_user_set')
    is_shared = models.BooleanField(default=False)
    sharer = models.ManyToManyField(User,related_name="sharer",blank=True)
    status_option= {
        ('Open','Open'),
        ('Confirmed','Confirmed'),
        ('Completed','Completed')
    }
    status = models.CharField(max_length=32, choices=status_option, default="Open")

    special_request = models.CharField(max_length=256,blank=True,default='')
    # vehicle = {
    #     (4, 'Sedan'),
    #     (5, 'SUV'),
    #     (6, 'Pickup'),
    #     (4, 'Coupe')
    # }
    special_vehicle_type = models.IntegerField(verbose_name="special_vehicle_type", choices=ThingPriority.choices, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        #(permission_code, human_readable_permission_name).
        permissions = (
            ("is_driver", "is_driver"),
        )
    

class RideSharer(models.Model):
    user_sharer = models.ForeignKey(User, related_name="user_share", on_delete=models.CASCADE)
    passenger_num = models.IntegerField(validators=[MinValueValidator(1)])
    joined_ride = models.ForeignKey(Ride, related_name="joinedride", on_delete=models.CASCADE)