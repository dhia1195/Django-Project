from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'destination', 'date', 'checkout_date', 'number_of_people', 'created_at')  # Updated to include new fields
    search_fields = ('name', 'email', 'destination')  # Enable search by name, email, and destination
    list_filter = ('date', 'number_of_people')  # Optional: add filters for date and number of people
