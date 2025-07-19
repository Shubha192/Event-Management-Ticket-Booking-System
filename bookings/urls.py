from django.urls import path
from . import views

urlpatterns = [
    path('new/<int:event_id>/', views.new_booking, name='new_booking'),
    path('mine/', views.my_bookings, name='my_bookings'),
]
