from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Ride, Driver, RideSharer
from django.core.mail import send_mass_mail,BadHeaderError
from django.contrib.auth.models import User, Permission 
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, StartRequestForm, JoinRequestForm, EditRequestForm, DriverRideForm, UserCreationForm, UserRegisterForm
from django.urls import reverse
from django import forms
from django.db.models import F
from django.core.mail import send_mass_mail,BadHeaderError
# # Create your views here.



@login_required
def home(request):
    # Render the HTML template index.html with the data in the context variable
    if request.user.is_authenticated:
        #print(request.user)
        orders_owner = list(Ride.objects.filter(owner=request.user))
        orders_sharer = list(Ride.objects.filter(sharer = request.user))
        context = {
            'orders_owner': orders_owner,
            'orders_sharer': orders_sharer
        }
    else:
        context = {}
    return render(request, 'user/home.html', context)




# dengyue-version
# def register(request):
#     if request.method == "GET":
#         return render(request, 'user/register.html')

#     user = request.POST.get("user")
#     password = request.POST.get("password")
#     email = request.POST.get("email")
#     #danger log 1: 判断为空，但其实可以在html使用requestuired字段实现
#     # if not email or not password or not user:
#     #     msg = "fill them"
#     #     return render(request, 'user/register.html', {'message': msg})
#     user_existed = User.objects.filter(username = user)
#     if user_existed:
#         msg = "username has been used!"
#         return render(request, 'user/register.html', {'message': msg})
#     email_existed = User.objects.filter(email = email)
#     if email_existed:
#         msg = "email has been used!"
#         return render(request, 'user/register.html', {'message': msg})
#     #添加到数据库
#     user = User.objects.create_user(user, email, password)
#     user.save()
#     message = "Register successfully!"
#     return render(request, 'user/home.html', {'message': message})



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            
            new_user = form.cleaned_data['username']
            new_email = form.cleaned_data.get('email')
            user_existed = User.objects.filter(username = new_user)
            print(new_user)
            if user_existed:
                msg = "username has been used!"
                return render(request, 'user/register.html', {'message': msg})
            email_existed = User.objects.filter(email = new_email)
            if email_existed:
                msg = "email has been used!"
                return render(request, 'user/register.html', {'message': msg})


            form.save()
            msg = "Your account has been created! You are now able to log in!"
            # 
            return render(request, 'user/home.html', {'message':msg})
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form':form})


# def login(request):
#     # login_form = forms.UserForm()
#     # if request.session.get('is_login', None):  # 不允许重复登录
#     #     return redirect('/index/')
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         message = 'please check the input information!'
#         if login_form.is_valid():
#             username = login_form.cleaned_data.get('username')
#             password = login_form.cleaned_data.get('password')

#             try:
#                 user = User.objects.get(name=username)
#             except :
#                 message = 'user not exist!'
#                 return render(request, 'login/login.html', locals())
#             if user.password == password:
#                 request.session['is_login'] = True
#                 request.session['user_id'] = user.id
#                 request.session['user_name'] = user.username
                
#                 # orders = Order.objects.all()
#                 # 指定渲染模板并传递数据
#                 # return render(request, 'login/mainpage.html', locals())
#                 return redirect('user/home.html')
#             else:
#                 message = 'password not correct!'
#                 return render(request, 'login/login.html', locals())
#         else:
#             return render(request, 'login/login.html', locals())

#     # login_form = forms.UserForm()
#     return render(request, 'login/login.html', locals())

@login_required
def start_request(request):
    if request.method == 'POST':
        form = StartRequestForm(request.POST)
        if form.is_valid():
            # print(request.user)
            #need to check if orders have time overlap -- which is unaccepted!!

            ride = form.save()
            ride.owner = request.user
            ride.save()
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('home')
    else:
        form = StartRequestForm()
    return render(request, 'user/start_request.html', {'form':form})

@login_required
def user_order(request):
    own_orders = list(Ride.objects.filter(owner=request.user))
    share_orders = list(Ride.objects.filter(sharer = request.user))
    context = {
        'ride_own': own_orders, 
        'ride_share' : share_orders
    }
    return render(request, 'user/home.html', context)

@login_required
def edit_request(request, nid):
    obj = Ride.objects.filter(id=nid).first()
    if obj.status!="Open":
        msg = "Order confirmed, can't make changes"
        return render(request, 'user/index.html', {"message":msg})
    if request.method == "GET":
        form = EditRequestForm(instance = obj)
        return render(request, 'user/edit_request.html', {"form": form})
    form = EditRequestForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'user/edit_request.html', {"form": form})

def delete_request(request, nid):
    ride = Ride.objects.filter(id=nid).first()
    if ride.status!="Open":
        msg = "Order confirmed, can't make changes"
        return render(request, 'user/index.html', {"message":msg})
    Ride.objects.filter(id=nid).first().delete()
    return redirect('home')

def request_detail(request, nid):
    ride = Ride.objects.filter(id=nid).first()
    context = {
        'ride': ride
    }
    return render(request, 'user/request_detail.html', context)

@login_required
def join_request(request, nid, num):
    # this is a GET method

    Ride.objects.filter(id=nid).update(passenger_number=F('passenger_number') + num)
    ride = Ride.objects.filter(id=nid).first()
    ride.sharer.add(request.user)
    # sharer_list = ride.sharer_number_list
    # sharer_list[request.user.get_uesrname()] = num
    ride.save()
    sharer = RideSharer.objects.create(user_sharer=request.user, passenger_num=num,joined_ride=ride)
    # obj.save()
    #print(Ride.objects.filter(id=nid).first().passenger_number)
    # context = {
    #     'num': num
    # }
    return redirect('home')

@login_required
def quit_request(request, nid):
    ride = Ride.objects.filter(id=nid).first()
    if ride.status!="Open":
        msg = "Order confirmed, can't make changes"
        return render(request, 'user/index.html', {"message":msg})
    sharer = RideSharer.objects.filter(joined_ride=ride).filter(user_sharer=request.user).first()
    num = sharer.passenger_num
    Ride.objects.filter(id=nid).first().sharer.remove(request.user)
    Ride.objects.filter(id=nid).update(passenger_number=F('passenger_number') - num)
    # Ride.objects.filter(id=nid).first().update(passenger_number=F('passenger_number') - num)
    return redirect('home')

@login_required
def search_ride(request):
    if request.method == "POST":
        form = JoinRequestForm(request.POST)
        if form.is_valid():
            #!!! to be added: need to check if orders have time overlap -- which is unaccepted!!

             
            ans = Ride.objects.filter(status="Open").filter(is_shared=True)
            ans = ans.exclude(owner__exact=request.user).exclude(sharer__exact=request.user)
            # 1. sharer has a special vehicle type request
            if (form.cleaned_data['special_vehicle_type'] != None):               
                ans = ans.filter(special_vehicle_type__exact=form.cleaned_data['special_vehicle_type']).filter(special_vehicle_type__gte= F('passenger_number')+form.cleaned_data['passenger_number'])
            # 2. sharer does not have a special vehicle type request
            else:
                ans_not_special = ans.filter(special_vehicle_type=None).filter(passenger_number__lte=6-form.cleaned_data['passenger_number'])
                ans_special = ans.filter(special_vehicle_type__gte= F('passenger_number')+form.cleaned_data['passenger_number'])
                ans = ans_special | ans_not_special
            ans = ans.filter(destination__exact=form.cleaned_data['destination'])
            ans = ans.filter(arrival_time__gte = form.cleaned_data['earliest_time']).filter(arrival_time__lte = form.cleaned_data['latest_time'])

            context = {
                'ans': ans,
                'num': form.cleaned_data['passenger_number']
            }
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'Your account has been created! You are now able to log in')
            return render(request, 'user/show_available_ride.html', context)
    else:
        form = JoinRequestForm()
    return render(request, 'user/search_ride.html', {'form':form})



@login_required
def driver_register(req):
    user = req.user
    if Driver.objects.filter(user_id=user.id).count()>0:
        msg = "You have already registered as a driver!"
        return render(req, 'user/index.html', {'message': msg})
    if req.method == "GET":
        return render(req, 'user/driver_register.html')
    received_data = req.POST
    #print(received_data.get("capacity"))
    vehicle_type=received_data.get("vehicle")
    plate_num=received_data.get("plate")
    plate_existed = Driver.objects.filter(plate_num = plate_num)
    if plate_existed:
        msg = "Plate number already registered!"
        return render(req, 'user/driver_register.html', {'message': msg})
    driver = Driver.objects.create(user=req.user, 
                    vehicle_type=received_data.get("vehicle"),
                    plate_num=received_data.get("plate"),
                    capacity= vehicle_type,
                    special_vehicle_info=received_data.get("special_info"))
    
    perm = Permission.objects.get(codename='is_driver')
    user.user_permissions.add(perm) 
    print(user.has_perm('user.is_driver'))
    driver.save()
    user.save()
    msg = "Great, you are a driver now!"
    return redirect('driver_site')

@login_required
def user_info(req):
    user = req.user
    is_driver = Driver.objects.filter(user_id=user.id).count()
    if req.method == "GET":
        driver_info = None
        plate_type = None
        if Driver.objects.filter(user_id=user.id).count() > 0:
            driver_info = Driver.objects.get(user=req.user)
            plate_type = driver_info.get_vehicle_type_display()
        username = User.objects.get(username=req.user).username
        email = User.objects.get(username=req.user).email
        context = {
            'username':username, 
            'email':email,
            'is_driver':is_driver,
            'plate_type':plate_type
        }
        return render(req, 'user/user_info.html', {'driver': driver_info,'context':context})
    data = req.POST
    if Driver.objects.filter(user_id=user.id).count() > 0:
        driver_info = Driver.objects.get(user=user)
        driver_info.plate_num = data.get("plate")
        if data.get("vehicle_type")!=None:
            driver_info.vehicle_type = data.get("vehicle_type")
            driver_info.capacity = driver_info.vehicle_type
        driver_info.special_vehicle_info = data.get("vehicle_info")
        print(driver_info.get_vehicle_type_display())
        driver_info.save()
    user_info = User.objects.get(username=user)
    user_info.username = data['name']
    user_info.email = data['email']
    user_info.save()
    msg = "Saved!"
    return redirect(reverse('user_info'))


@login_required
# @permission_required('user.is_driver', login_url='/driver_register/')
def driver_site(req):
    if Driver.objects.filter(user=req.user).count() > 0:

        return render(req, 'user/driver_site2.html')
    else:
        return redirect('driver_register')




@login_required
def driver_unregister(req):
    # ride_id = req.session.get('ride_id')
    if not Driver.objects.filter(user_id=req.user.id).count()>0:
        print("ssssss")
        return redirect('driver_register')
    if req.method == "POST":
        print("post")
        ride = Ride.objects.filter(driver = req.user, status = 'Confirmed')
        if ride :
            msg = 'Sorry, you have unfinished rides.'
            return render(req, 'user/driver_site.html', {'message' : msg})
        perm = Permission.objects.get(codename='is_driver')
        driver = Driver.objects.get(user=req.user)
        driver.delete()
        req.user.user_permissions.remove(perm) 
        req.user.save()
        msg = 'Okay, you are no longer a driver anymore.'
        return redirect( 'home')
    else:
        print("still here")
        return render(req, 'user/driver_unregister.html')


def match(driver, user):

    mathched_rides1 = Ride.objects.filter(
        status='Open',
        special_vehicle_type = None,
        passenger_number__lte = driver.capacity,
        driver = None 
    )

    mathched_rides2 = Ride.objects.filter(
        status = 'Open',
        ##consider
        special_vehicle_type = driver.vehicle_type,
        passenger_number__lte = driver.capacity,
        driver = None 
    )
    mathched_rides = mathched_rides1 | mathched_rides2
    print(mathched_rides2.count())
    mathched_rides = mathched_rides.exclude(owner = user)
    mathched_rides = mathched_rides.exclude(sharer = user)
    return mathched_rides

# task 15
@login_required
def driver_search(req):
    if req.method == "GET":
        user = req.user
        driver = Driver.objects.get(user = user)
        mathched_rides = match(driver, user)
        context = {
            'rides' : mathched_rides,
        }
        #examine data
        #form = DriverRideForm(data = mathched_rides)
        # if form.is_valid():
        return render(req, 'user/driver_search.html', context)
    ride_id = req.session.get('ride_id')
    user = req.user
    ride = Ride.objects.get(pk = ride_id)
    driver = Driver.objects.get(pk = user)
    #可以考虑删除
    if ride.status != 'Open':
        msg = "This ride has been confirmed by others!"
        return render(req, 'user/driver_search.html', {"messege" : msg})
    if ride.special_vehicle_type and ride.special_vehicle_type != driver.vehicle_type:
        msg = "This ride request other vehicle type!"
        return render(req, 'user/driver_search.html', {"messege" : msg})
    if ride.passenger_number > driver.capacity:
        msg = "This ride request more capacity!"
        return render(req, 'user/driver_search.html', {"messege" : msg})
    ride.driver = driver
    ride.status = "Confirmed"
    ride.save()
    msg = "You have confirmed a ride!"
    return render(req, 'user/driver_search.html', {"messege" : msg})

# task 16/17
@login_required

def driver_confirm(req, ride_id):
    ride = Ride.objects.get(pk = ride_id)
    user = User.objects.get(username = req.user.username)
    driver = Driver.objects.get(user = user)
    if ride.status != 'Open':
        msg = "This ride has been confirmed by others!"
        return render(req, 'user/driver_confirm.html')
    if ride.special_vehicle_type and ride.special_vehicle_type != driver.vehicle_type:
        msg = "This ride request other vehicle type!"
        return render(req, 'user/driver_confirm.html', {"messege" : msg})
    ride.driver = user
    ride.status = "Confirmed"
    #task 17
    send_email_data(ride, user)
    msg = "You have confirmed a ride!"
    ride.save()
    return redirect('driver_search')

#task 17
def send_email_data(ride, user):
    sbj = "Ride confirmed"
    msg = "Your ride to " + ride.destination + " is claimed by " + user.username
    emails = [
        (sbj, msg, 'yd171@outlook.com', [ride.owner.email]),
    ]
    if ride.sharer:
        for sharer in ride.sharer.all():
            msgs = (sbj, msg, None, [User.objects.get(username = sharer).email])
            emails.append(msgs)
    try:
        send_mass_mail(emails, fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

#task 18
@login_required
def driver_order(req):
    user = req.user
    confirmed_rides = Ride.objects.filter(driver = user, status = "Confirmed")
    completed_rides = Ride.objects.filter(driver = user, status = "Completed")
    context = {
        'rides' : confirmed_rides,
        'completed' : completed_rides
    }
    #examine data
    #form = DriverRideForm(data = mathched_rides)
    # if form.is_valid():
    return render(req, 'user/driver_order.html', context)

@login_required
def complete_order(req, ride_id):
    # ride_id = req.session.get('ride_id')
    ride = Ride.objects.get(pk = ride_id)
    print('fdsaffsdafasd')
    ride.status = "Completed"
    ride.save()
    msg = "Order Completed!!"
    return render(req, 'user/complete_order.html', {'message': msg})
