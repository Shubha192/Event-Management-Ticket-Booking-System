from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    num_tickets = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
