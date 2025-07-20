
from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.my_bookings, name='my_bookings'),
    path('<int:event_id>/new/', views.new_booking, name='new_booking'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('<int:booking_id>/download/', views.download_ticket, name='download_ticket'),
]
