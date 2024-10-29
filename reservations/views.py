import io
import os
import requests
import base64  # Ensure base64 is imported
from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation  # Ensure the correct import path for your Reservation model
from django.conf import settings
from user_client.models import User_client

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
HEADERS = {"Authorization": "Bearer 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"}

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

            # Call the Hugging Face API to generate an image
            payload = {"inputs": destination}
            response = requests.post(API_URL, headers=HEADERS, json=payload)

            image_url = None
            if response.status_code == 200:
                # Process the response to get the image
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))

                # Ensure the media/images directory exists
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'images'), exist_ok=True)

                # Save the generated image to a desired path
                image_filename = f"{name.replace(' ', '_')}_image.png"
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_filename)
                image.save(image_path, format='PNG')  # Specify the format
                image_url = f"/media/images/{image_filename}"  # URL for accessing the image
            else:
                error_message = response.json().get('error', 'Image generation failed.')
                messages.error(request, f'Image generation failed: {error_message}')

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
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Reservation added successfully!', 'image_url': image_url})

            # Add a success message for regular requests
            messages.success(request, 'Reservation added successfully!')
            return redirect('front')  # Redirect for normal requests

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': str(e)})
    user_id = request.session.get('user_id')  # Get the user ID from session
    user = None
    if user_id:
        try:
            user = User_client.objects.get(id=user_id)  # Get the user from the database
        except User_client.DoesNotExist:
            user = None
    return render(request, 'index.html',{'user': user})

def get_image_for_destination(request):
    destination = request.GET.get('destination')

    if destination:
        try:
            # Generate a new image for the destination using Hugging Face API
            payload = {"inputs": destination}
            response = requests.post(API_URL, headers=HEADERS, json=payload)

            if response.status_code == 200:
                # Process the response to get the image
                image_bytes = response.content

                # Load and encode the generated image in base64
                base64_encoded_image_data = base64.b64encode(image_bytes).decode('utf-8')
                return JsonResponse({'image_data': base64_encoded_image_data})

            # If the response was not successful, log the error and return a message
            error_message = response.json().get('error', 'Failed to generate image.')
            print(f"API Error: {error_message}")  # Log the API error
            return JsonResponse({'error': f'Failed to generate image for "{destination}": {error_message}'}, status=500)

        except requests.exceptions.RequestException as e:
            # Handle requests-specific exceptions
            print(f"Request exception: {str(e)}")
            return JsonResponse({'error': 'Error while contacting the image generation service.'}, status=500)
        except Exception as e:
            # Catch-all for any other exceptions
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No destination provided'}, status=400)
