from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Ride, Driver
from django.contrib.auth.models import User, Permission
from datetime import datetime, timedelta, tzinfo
from django.utils import timezone

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     #is_driver = forms.BooleanField()
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']


# class RegisterForm(forms.Form):
#     username = forms.CharField(label="user name", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label="password again", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label="email address", widget=forms.EmailInput(attrs={'class': 'form-control'}))

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #is_driver = forms.BooleanField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RegisterForm(ModelForm):
    class Meta: 
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class StartRequestForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['destination', 'arrival_time', 'passenger_number', 'is_shared', 'special_vehicle_type' ,'special_request' ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class EditRequestForm(ModelForm):
    class Meta:
        model = Ride
        fields = ['destination', 'arrival_time', 'passenger_number', 'is_shared', 'special_vehicle_type' ,'special_request' ]




class JoinRequestForm(ModelForm):
    earliest_time = forms.DateTimeField(initial=timezone.now)
    latest_time = forms.DateTimeField(initial=timezone.now)

    class Meta:
        model = Ride
        fields = ['destination', 'passenger_number', 'special_vehicle_type', 'special_request', 'earliest_time', 'latest_time']



# class RideRequestForm(forms.ModelForm):
#     destination = forms.CharField()
#     arrival_time = forms.DateTimeField()
#     passenger_number = forms.IntegerField()
#     #is_shared = forms.ChoiceField(initial=2,choices=((1, 'True'),(2,'False')))
#     special_request = forms.CharField()
#     special_vehicle_type = forms.CharField(required=False)    
#     class Meta:
#         model = Ride
#         fields = ['destination', 'arrival_time', 'passenger_number', 'vehicle_type', 'special_request', 'can_Shared']


class DriverRideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['destination', 'arrival_time',
        'passenger_number', 'owner', 'driver', 'is_shared', 'sharer',
        'status', 'special_request', 'special_vehicle_type']
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class" : "form-control", "placeholder": field.label}

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class" : "form-control", "placeholder": field.label}