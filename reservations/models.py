from django.db import models
from activite.models import Activite 
class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=100)
    date = models.DateField()  # Check-in date
    checkout_date = models.DateField(null=True)  # Allow null temporarily
    number_of_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Allow null temporarily
    updated_at = models.DateTimeField(auto_now=True)  

    activite = models.ForeignKey(Activite, on_delete=models.CASCADE, related_name="reservations", null=True, blank=True) 

    def __str__(self):
        return f"{self.name} - {self.destination} ({self.date} to {self.checkout_date})"
