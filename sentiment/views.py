import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Avis, AnalyseSentiment

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
HEADERS = {"Authorization": "Bearer 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"}

@csrf_exempt
def sentiment_analysis_view(request):
    if request.method == 'POST':
        utilisateur = request.POST.get('utilisateur')
        destination = request.POST.get('destination')
        commentaire = request.POST.get('commentaire')
        note = int(request.POST.get('note', 0))  # Handle missing or invalid note gracefully

        # Create a new 'Avis' record
        avis = Avis.objects.create(
            utilisateur=utilisateur,
            destination=destination,
            commentaire=commentaire,
            note=note
        )

        # Call the Hugging Face API
        payload = {"inputs": commentaire}
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            sentiment_data = response.json()

            if isinstance(sentiment_data, list) and sentiment_data:
                sentiment = sentiment_data[0][0]
                sentiment_label = sentiment.get('label', 'LABEL_1')
                score = sentiment.get('score', 0.0)

                # Save the sentiment analysis result
                AnalyseSentiment.objects.create(
                    avis=avis,
                    sentiment=sentiment_label.lower(),
                    score=score
                )

                return JsonResponse({
                    'success': True,
                    'sentiment': sentiment_label,
                    'score': score
                })

            return JsonResponse({'success': False, 'message': 'Invalid API response.'})
        print("API Error:", response.status_code, response.text)
        return JsonResponse({'success': False, 'message': 'API request failed.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
