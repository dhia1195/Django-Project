from django.contrib import admin
from .models import User_client

# Register your models here.
@admin.register(User_client)
class User_clientAdmin(admin.ModelAdmin):
    pass  # This serves as a placeholder for now
