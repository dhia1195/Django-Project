import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from .models import TexteSource, TexteTraduit  # Ensure models are correctly imported

# Translation API configurations for French-to-English and Spanish-to-English
TRANSLATION_API_URLS = {
    "fr": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-fr-en",
    "es": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-es-en"
}
HEADERS = {"Authorization": "Bearer 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"}

@csrf_exempt
def translation_view(request):
    if request.method == 'POST':
        texte_source = request.POST.get('texte_source')
        langue_source = request.POST.get('langue_source')  # French or Spanish
        langue_cible = 'en'  # English as the target language

        # Save the source text to the database
        texte = TexteSource.objects.create(
            langue_source=langue_source,
            contenu=texte_source
        )

        # Select the correct API URL based on source language (French or Spanish)
        translation_api_url = TRANSLATION_API_URLS.get(langue_source)
        if not translation_api_url:
            return JsonResponse({'error': 'Unsupported source language'}, status=400)

        # API call to Hugging Face
        payload = {"inputs": texte_source}
        response = requests.post(translation_api_url, headers=HEADERS, json=payload)

        # Process API response
        if response.status_code == 200:
            data = response.json()
            texte_traduit = data[0].get('translation_text')  # Adjust if necessary

            # Save the translation in the database
            TexteTraduit.objects.create(
                texte_source=texte,
                langue_cible=langue_cible,
                texte_traduit=texte_traduit
            )

            # Return the translated text as a JSON response
            return JsonResponse({'translated_text': texte_traduit}, status=200)
        else:
            error_message = response.json().get('error', 'Erreur de traduction.')
            return JsonResponse({'error': f"Échec de la traduction : {error_message}"}, status=400)

    return render(request, 'index.html')


@csrf_exempt
def get_translations(request):
    if request.method == 'GET':
        # Retrieve all translations or apply filters if needed
        translations = TexteTraduit.objects.all()
        
        # Serialize the data to JSON format
        translations_data = serialize('json', translations)
        
        return JsonResponse({'translations': translations_data}, safe=False)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
