from django.shortcuts import render, redirect
from .models import Booking
from events.models import Event
from django.contrib.auth.decorators import login_required

@login_required
def new_booking(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == "POST":
        num_tickets = int(request.POST['num_tickets'])
        if num_tickets <= event.capacity:
            event.capacity -= num_tickets
            event.save()
            Booking.objects.create(user=request.user, event=event, num_tickets=num_tickets)
            return redirect('my_bookings')
    return render(request, 'bookings/new_booking.html', {'event': event})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
