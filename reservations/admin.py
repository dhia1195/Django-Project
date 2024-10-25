from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'number_of_people')  # Columns to display in the list view
    search_fields = ('name', 'email')  # Enable search by name or email
