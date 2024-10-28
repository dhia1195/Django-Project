from django.db import models

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=100)
    date = models.DateField()  # Check-in date
    checkout_date = models.DateField(null=True)  # Allow null temporarily
    number_of_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Allow null temporarily
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.name} - {self.destination} ({self.date} to {self.checkout_date})"
