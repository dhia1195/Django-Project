from django.contrib import admin
from .models import Activite

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'cout', 'duree', 'pax')  # Updated columns to display
    search_fields = ('nom', 'adresse')  # Enable search by name or address
    list_filter = ('cout', 'duree', 'pax')  # Optional: add filters for cost, evaluation, duration, and number of people

    fieldsets = (
        (None, {
            'fields': ('nom', 'adresse', 'cout', 'image', 'duree', 'pax')  # Include all fields
        }),
    )
