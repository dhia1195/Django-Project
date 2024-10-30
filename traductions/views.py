import requests
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from .models import TexteSource, TexteTraduit 
from langdetect import detect, DetectorFactory
 # Ensure models are correctly imported

# Translation API configurations for French-to-English and Spanish-to-English
# TRANSLATION_API_URLS = {
#     "fr": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-fr-en",
#     "es": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-es-en"
# }
HEADERS = {"Authorization": "Bearer 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"}

@csrf_exempt
# Set a seed for the random number generator to make the results deterministic
# DetectorFactory.seed = 0

# Assume TRANSLATION_API_URLS and HEADERS are defined elsewhere

def translation_view(request):
    if request.method == 'POST':
        texte_source = request.POST.get('texte_source')

        # Detect the source language using langdetect
        try:
            langue_source = detect(texte_source)
            print("hello",langue_source)
        except Exception as e:
            return JsonResponse({'error': f'Error in language detection: {str(e)}'}, status=500)

        langue_cible = 'en'  # English as the target language

        # Save the source text to the database
        texte = TexteSource.objects.create(
            langue_source=langue_source,
            contenu=texte_source
        )

        # Select the correct API URL based on detected source language
        translation_api_url = f'https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{langue_source}-en'
        # TRANSLATION_API_URLS.get(langue_source)
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
            # return redirect('front')
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
