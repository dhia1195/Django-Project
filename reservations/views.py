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
from django.core.serializers import serialize
from django.http import JsonResponse
from .models import Reservation
from user_client.models import User_client
from django.views.decorators.csrf import csrf_exempt
import json
import re
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch
import time

from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from activite.models import Activite  # Import the Activite model
import google.generativeai as genai




logger = logging.getLogger(__name__)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
API_URL2 = "https://api-inference.huggingface.co/models/google/flan-t5-large"
API_URL3 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1-base"
HEADERS = {"Authorization": "Bearer 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"}


def queryFood(payload):
    response = requests.post(API_URL2, headers=HEADERS, json=payload)
    return response.json()
def queryImage(payload):
    response1 = requests.post(API_URL3, headers=HEADERS, json=payload)
    
    if response1.status_code == 200:
        # Assuming the API returns an image directly
        # Save the image to a file or return the content
        return response1.content  # This returns the raw image data
    else:
        print("Error fetching data:", response1.status_code)
        return None
def wait_for_image_load(payload, timeout=1200):
    start_time = time.time()
    while True:
        image_data = queryImage(payload)
        if image_data:
            return image_data  # Image loaded successfully
        elif time.time() - start_time > timeout:
            print("Timeout waiting for image to load.")
            return None  # Return None if the timeout is reached
        time.sleep(1)  # Wait before trying again
def food_recommendation(country):
    print(f"What are some famous dishes to try in {country}?")
    foodR = queryFood({"inputs": f"What are some famous dishes to try in {country}?"})
    food_name=foodR[0]['generated_text']
    imageR=wait_for_image_load({"inputs": food_name})
     # Define the directory and image path
    image_dir = 'static/images'
    image_path = os.path.join(image_dir, f'{food_name}.jpg')
    image_name=f'{food_name}.jpg'    
     # Create the directory if it doesn't exist
    os.makedirs(image_dir, exist_ok=True)
    with open(image_path, 'wb') as img_file:
        img_file.write(imageR)
    ("Image saved at:", image_path)
    return food_name,image_name
    # print({food,image})

        

genai.configure(api_key=settings.GENAI_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def front_view(request):
    country_names = []
    foodR=''
    imageF=''
    response = requests.get("https://restcountries.com/v3.1/all") 
    if response.status_code == 200:
        data = response.json()
        # Extract country names
        country_names = [country['name']['common'] for country in data]
        
    else:
        print("Error fetching data:", response.status_code)
  
    if request.method == 'POST':
     if request.POST.get('country'):
            print('country')
            country_name=request.POST.get('country')
            result=food_recommendation(country_name)
            foodR=result[0]
            imageF=result[1]
            print(imageF)
            

     else:
        try:

            # Get data from the form
            name = request.POST.get('name') 
            email = request.POST.get('email')
            destination = request.POST.get('destination')
            number_of_people = request.POST.get('number_of_people')
            date = request.POST.get('date')
            checkout_date = request.POST.get('checkout_date')
            activite_id = request.POST.get('activite')
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
                checkout_date=checkout_date,
                activite_id=activite_id 
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
            user = User_client.objects.get(id=user_id)
            formatted_date = user.date_of_birth.strftime('%Y-%m-%d')  # Get the user from the database
        except User_client.DoesNotExist:
            user = None
    activities = Activite.get_activities_with_captions()  # Fetch all activities      
    return render(request, 'index.html',{'activities': activities,'user': user, 'formatted_date': formatted_date,'countries':country_names,'foodR':foodR,'imageF':imageF})
            
   
   


def get_reservations(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Serialize only the fields you need for each reservation
        reservations = Reservation.objects.all().values(
            'id', 'name', 'email', 'destination', 'number_of_people', 'date', 'checkout_date', 'activite__nom'
        )
        return JsonResponse({'reservations': list(reservations)}, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@require_POST
def update_reservation(request, reservation_id):
    try:
        data = json.loads(request.body)
        reservation = Reservation.objects.get(id=reservation_id)
        
        # Update fields and log the data for debugging
        reservation.name = data.get('name', reservation.name)
        reservation.email = data.get('email', reservation.email)
        reservation.destination = data.get('destination', reservation.destination)
        reservation.number_of_people = data.get('number_of_people', reservation.number_of_people)
        reservation.date = data.get('date', reservation.date)
        reservation.checkout_date = data.get('checkout_date', reservation.checkout_date)
        
        
        reservation.save()  # Attempt to save to DB
        logger.info(f"Updated reservation {reservation_id} successfully.")
        
        return JsonResponse({'success': True, 'message': 'Reservation updated successfully.'})
    except Reservation.DoesNotExist:
        logger.error(f"Reservation with id {reservation_id} does not exist.")
        return JsonResponse({'success': False, 'message': 'Reservation not found.'}, status=404)
    except Exception as e:
        logger.error(f"Error updating reservation {reservation_id}: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@csrf_exempt  # Temporarily disable CSRF protection for testing
def delete_reservation(request, reservation_id):
    if request.method == 'DELETE':
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()
            return JsonResponse({'success': True, 'message': 'Reservation deleted successfully.'})
        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reservation not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
    
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
@csrf_exempt
def chat_interaction(request):
    if request.method == 'POST':
        question = request.POST.get('msg')  # Get the question from the POST data
        if not question or not question.strip():
            return JsonResponse({'error': 'No question provided'}, status=400)

        # Generate a response using the chat model
        response = chat.send_message(question)
        response_text = response.text

        return JsonResponse({'response': response_text})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)