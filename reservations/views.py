# reservations/views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from .models import Reservation

def front_view(request):
    if request.method == 'POST':
        try:
            # Get data from the form
            name = request.POST.get('name')
            email = request.POST.get('email')
            destination = request.POST.get('destination')
            number_of_people = request.POST.get('number_of_people')
            date = request.POST.get('date')
            checkout_date = request.POST.get('checkout_date')

            # Create a new reservation
            Reservation.objects.create(
                name=name,
                email=email,
                destination=destination,
                number_of_people=number_of_people,
                date=date,
                checkout_date=checkout_date
            )

            # If AJAX request, return JSON response
            if request.is_ajax():
                return JsonResponse({'success': True, 'message': 'Reservation added successfully!'})

            # Add a success message for regular requests
            messages.success(request, 'Reservation added successfully!')
            return redirect('front')  # Redirect for normal requests

        except Exception as e:
            if request.is_ajax():
                return JsonResponse({'success': False, 'message': str(e)})

    # Render the page with any messages
    return render(request, 'index.html')
