from django.contrib import admin
from .models import Activite

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'horaire', 'cout', 'evaluation')  # Columns to display in the list view
    search_fields = ('nom', 'adresse')  # Enable search by name or address
