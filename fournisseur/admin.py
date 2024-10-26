from django.contrib import admin
from .models import Fournisseur

class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_service', 'adresse', 'telephone', 'email', 'evaluation')
    search_fields = ('nom', 'type_service', 'adresse')

admin.site.register(Fournisseur, FournisseurAdmin)
