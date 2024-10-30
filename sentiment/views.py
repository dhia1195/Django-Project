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
        note = int(request.POST.get('note'))

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

            # Ensure valid API response
            if isinstance(sentiment_data, list) and sentiment_data:
                sentiment = sentiment_data[0][0]  # Get first sentiment
                sentiment_label = sentiment['label']
                score = sentiment['score']

                # Save sentiment to database
                AnalyseSentiment.objects.create(
                    avis=avis,
                    sentiment=sentiment_label.lower(),
                    score=score
                )

                # Return JSON response
                return JsonResponse({
                    'success': True,
                    'sentiment': sentiment_label,
                    'score': score
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid response format.'})

        return JsonResponse({'success': False, 'message': 'API request failed.'})

    return render(request, 'index.html')
