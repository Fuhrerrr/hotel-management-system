from django.urls import path 
from django.contrib.auth import views as auth_views

from user_dashboard import views


app_name = "dashboard"


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("booking-detail/<booking_id>/", views.booking_detail, name="booking_detail"),
    path("bookings/", views.bookings, name="bookings"),
    path("notifications/", views.notifications, name="notifications"),
    path("wallet/", views.wallet, name="wallet"),
    path("bookmark/", views.bookmark, name="bookmark"),
    path("delete_bookmark/<bid>/", views.delete_bookmark, name="delete_bookmark"),
    path("profile/", views.profile, name="profile"),

    # Change Password View
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='user_dashboard/password-reset/change-password.html',success_url = '/dashboard/password-changed/'),name='change_password'),
    path("password-changed/", views.password_changed, name="password_changed"),


    # Ajax
    path("notification_filter/", views.notification_filter, name="notification_filter"),
    path("notification_mark_as_seen/", views.notification_mark_as_seen, name="notification_mark_as_seen"),
    path("add_to_bookmark/", views.add_to_bookmark, name="add_to_bookmark"),
    path("add_review/", views.add_review, name="add_review"),

]