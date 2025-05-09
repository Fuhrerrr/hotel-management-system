from django.urls import path 
from hotel import views 

app_name = "hotel"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<slug:slug>/", views.hotel_detail, name="detail"),
    path("detail/<slug:slug>/room-type/<slug:rt_slug>/", views.room_type_detail, name="room_type_detail"),
    path("selected_rooms/", views.selected_rooms, name="selected_rooms"),
    path("checkout/<booking_id>/", views.checkout, name="checkout"),
    path("invoice/<booking_id>/", views.invoice, name="invoice"),
    path("update_room_status/", views.update_room_status, name="update_room_status"),
    
    # Payment API
    path('api/checkout-session/<booking_id>/', views.create_checkout_session, name='api_checkout_session'),
    path('success/<booking_id>/', views.payment_success, name='success'),
    path('failed/<booking_id>/', views.payment_failed, name='failed'),
]