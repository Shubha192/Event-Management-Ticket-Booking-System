import os
import qrcode
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.conf import settings
from .models import Booking
from events.models import Event


def generate_qr_and_pdf(booking):
    # Make sure media folders exist
    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'tickets')
    os.makedirs(qr_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    # QR code
    qr = qrcode.make(f"Booking ID: {booking.id}")
    qr_path = os.path.join(qr_dir, f"booking_{booking.id}.png")
    qr.save(qr_path)

    # PDF
    pdf_path = os.path.join(pdf_dir, f"booking_{booking.id}.pdf")
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 800, f"Booking Confirmation for {booking.event.title}")
    c.drawString(100, 780, f"Booking ID: {booking.id}")
    c.drawString(100, 760, f"Tickets: {booking.num_tickets}")
    c.drawString(100, 740, f"User: {booking.user.username}")
    c.drawImage(qr_path, 100, 600, width=150, height=150)
    c.save()

    return pdf_path


@login_required
def new_booking(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        num_tickets = int(request.POST['num_tickets'])
        if num_tickets <= event.capacity:
            event.capacity -= num_tickets
            event.save()
            booking = Booking.objects.create(user=request.user, event=event, num_tickets=num_tickets)

            pdf_path = generate_qr_and_pdf(booking)

            # Email
            email = EmailMessage(
                subject='Your Booking Confirmation',
                body=f'Your booking for {event.title} is confirmed.',
                to=[request.user.email]
            )
            email.attach_file(pdf_path)
            email.send()

            return redirect('my_bookings')
        else:
            return render(request, 'bookings/new_booking.html', {
                'event': event,
                'error': 'Not enough tickets available.'
            })

    return render(request, 'bookings/new_booking.html', {'event': event})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.event.capacity += booking.num_tickets
    booking.event.save()
    booking.delete()
    return redirect('my_bookings')


@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'tickets', f'booking_{booking.id}.pdf')
    return FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename=f'ticket_{booking.id}.pdf')
