from django.shortcuts import render
from .models import Activite
import requests
from .models import generate_activity_tags
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)


API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def get_activities_with_captions():
    activities = Activite.objects.all()  # Fetch activities from the database
    for activity in activities:
        caption = generate_image_caption(activity.image.path)  # Generate captions
        activity.caption = caption  # Add caption to the activity
    return activities


@require_GET
def generate_activity_tags_view(request):
    image_path = request.GET.get('image_path')
    activity_name = request.GET.get('activity_name')
    price = request.GET.get('price')

    if not image_path or not activity_name or not price:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        price_value = float(price)  # Ensure the price is a float
    except ValueError:
        return JsonResponse({'error': 'Invalid price value'}, status=400)
    # Build the full path to check existence
    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path.lstrip('/'))
    logger.debug(f"Full image path: {full_image_path}")

    if not os.path.exists(full_image_path):
        return JsonResponse({'error': 'Image file does not exist.'}, status=404)

    tags = generate_activity_tags(full_image_path, activity_name, price_value)

    return JsonResponse({'tags': tags})