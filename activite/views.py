from django.shortcuts import render
from .models import Activite
from django.http import JsonResponse


def get_activities(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Serialize only the fields you need for each activity
        activities = Activite.objects.all().values(
            'id', 'nom', 'adresse', 'cout', 'duree', 'pax', 'image'  # Adjust fields as necessary
        )
        return JsonResponse({'activities': list(activities)}, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def activite_list(request):
    activities = Activite.objects.all()  # Fetch all activities or apply filters if needed
    return render(request, 'index.html', {'activities': activities})