from django.shortcuts import render
from .models import Activite

def front_view(request):
    activities = Activite.objects.all()  # Get all activities
    return render(request, 'index.html', {'activities': activities})