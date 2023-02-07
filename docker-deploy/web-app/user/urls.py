from django.urls import path, include
from django.contrib import admin 

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('driver_site/', views.driver_site, name='driver_site'),
    path('register/', views.register, name='register'),
    # path('login/', views.login, name='login'),
    path('start_request/', views.start_request, name='start_request'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('request_detail/<int:nid>/', views.request_detail, name='request_detail'),
    path('<int:nid>/edit_request/', views.edit_request, name='edit_request'),
    path('<int:nid>/delete_request/', views.delete_request, name='delete_request'),
    path('search_ride/', views.search_ride, name='search_ride'),
    path('join_request/<int:nid>/<int:num>', views.join_request, name='join_request'),
    path('quit_request/<int:nid>/', views.quit_request, name='quit_request'),
    path('driver_register/', views.driver_register, name='driver_register'),
    path('driver_unregister/', views.driver_unregister, name='driver_unregister'),
    path('driver_search/', views.driver_search, name='driver_search'),
     path('driver_order/', views.driver_order, name='driver_order'),
    path('<int:ride_id>/complete_order/', views.complete_order, name='complete_order'),
    # path('order_detail/<int:ride_id>/', views.order_detail, name='order_detail'),
    path('driver_confirm/<int:ride_id>/', views.driver_confirm, name='driver_confirm'),
     path('user_info/', views.user_info, name='user_info'),
    
]