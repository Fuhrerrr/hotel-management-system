from django.shortcuts import render, redirect
from django.db import models
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hotel.models import Booking, Notification, Bookmark, Hotel, Review
from userauths.models import Profile, User
from userauths.forms import ProfileUpdateForm, UserUpdateForm

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user, payment_status="paid")
    total_spent = Booking.objects.filter(user=request.user, payment_status="paid").aggregate(amount=models.Sum('total'))

    print("bookings ========", total_spent)
    context = {
        "bookings":bookings,
        "total_spent":total_spent,
    }
    return render(request, "user_dashboard/dashboard.html", context)

@login_required
def booking_detail(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)

    context = {
        "booking":booking,
    }
    return render(request, "user_dashboard/booking_detail.html", context)

@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user, payment_status="paid")

    context = {
        "bookings":bookings,
    }
    return render(request, "user_dashboard/bookings.html", context)


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)

    context = {
        "notifications":notifications,
    }
    return render(request, "user_dashboard/notifications.html", context)

def notification_filter(request):
    query = request.GET['query']
    if query == "all":
        notifications = Notification.objects.filter(user=request.user)
    elif query == "read":
        notifications = Notification.objects.filter(user=request.user, seen=True)
    elif query == "unread":
        notifications = Notification.objects.filter(user=request.user, seen=False)
    else:
        notifications = Notification.objects.filter(user=request.user)
    
    print("notifications ===", notifications)

    context = render_to_string("user_dashboard/async/notifications.html", {"notifications":notifications})
    print("data ======", context)

    return JsonResponse({"data":context})


def notification_mark_as_seen(request):
    id = request.GET['id']
    notification = Notification.objects.get(id=id)
    notification.seen = True
    notification.save()
    
    return JsonResponse({"data":"Marked As Seen"})


@login_required
def wallet(request):
    bookings = Booking.objects.filter(user=request.user, payment_status="paid")
    total_spent = Booking.objects.filter(user=request.user, payment_status="paid").aggregate(amount=models.Sum('total'))

    context = {
        "bookings":bookings,
        "total_spent":total_spent,
    }
    return render(request, "user_dashboard/wallet.html", context)



@login_required
def bookmark(request):
    bookmark = Bookmark.objects.filter(user=request.user)

    context = {
        "bookmark":bookmark,
    }
    return render(request, "user_dashboard/bookmark.html", context)



@login_required
def delete_bookmark(request, bid):
    bookmark = Bookmark.objects.filter(bid=bid)
    bookmark.delete()
    return redirect("dashboard:bookmark")


def add_to_bookmark(request):
    id = request.GET['id']
    hotel = Hotel.objects.get(id=id)
    if request.user.is_authenticated:
        bookmark = Bookmark.objects.filter(user=request.user, hotel=hotel)
        if bookmark.exists():
            bookmark = Bookmark.objects.get(user=request.user, hotel=hotel)
            bookmark.delete()
            return JsonResponse({"data":"Bookmark Deleted", "icon":"success"})
        else:
            Bookmark.objects.create(user=request.user, hotel=hotel)
            return JsonResponse({"data":"Hotel Bookmarked" , "icon":"success"})
    else:
        return JsonResponse({"data":"Login To Bookmark Hotel" , "icon":"warning"})


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect("dashboard:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        "profile":profile,
        "u_form":u_form,
        "p_form":p_form,
    }
    return render(request, "user_dashboard/profile.html", context)


@login_required
def password_changed(request):
    return render(request, "user_dashboard/password_changed.html")


@login_required
def add_review(request):
    id = request.GET['id']
    rating = request.GET['rating']
    review = request.GET['review']
    hotel = Hotel.objects.get(id=id)

    review_check = Review.objects.filter(user=request.user, hotel=hotel)
    if review_check.exists():
        return JsonResponse({"data":"Review Already Exists", "icon":"warning"})
    else:
        Review.objects.create(
            user=request.user,
            rating=rating,
            hotel=hotel,
            review=review
        )
        return JsonResponse({"data":"Review Submitted, Thank You." , "icon":"success"})