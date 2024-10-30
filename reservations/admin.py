from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'destination', 'date', 'checkout_date', 'number_of_people', 'activite', 'created_at')  # Added activite field
    search_fields = ('name', 'email', 'destination')  # Enable search by name, email, and destination
    list_filter = ('date', 'number_of_people', 'activite')  # Add filter for activite as well

    # Optional: you can customize the form to include fields that are editable directly in the admin
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'destination', 'date', 'checkout_date', 'number_of_people', 'activite')
        }),
    )
