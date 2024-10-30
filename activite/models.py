from django.db import models
import requests
import os
import base64
import time



API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def get_image_tags(image_path):
    try:
        with open(image_path, "rb") as f:
            img = f.read()
    except Exception as e:
        print(f"Error reading image: {e}")
        return []

    # Prepare the payload with base64-encoded image data
    payload = {
        "parameters": {
            "candidate_labels": [
                "landscape", "water", "sunset", "mountains",
                "ocean", "forest",
                "hiking", "biking", "exploration"
            ]
        },
        "inputs": base64.b64encode(img).decode("utf-8")
    }

    # Attempt to query the API with retries for 5 attempts
    for attempt in range(5):
        response = requests.post("https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14", headers=headers, json=payload)
        
        if response.status_code == 200:
            output = response.json()
            print("API Response Output:", output)  # For debugging
            # Extract tags based on confidence scores
            tags = [item['label'] for item in output if item['score'] > 0.1]
            return tags
        elif response.status_code == 400:
            print(f"Bad Request: {response.json()}")  # Log detailed error message
            return []
        elif response.status_code == 503:
            time.sleep(attempt + 1)  # Exponential backoff for 503 errors
        else:
            print(f"Error: Received status code {response.status_code}")  # Log any other errors
            return []

    return []




def get_text_tags(activity_name):
    # Construct the payload for the API request
    payload = {
        "inputs": activity_name,
        "parameters": {
            "candidate_labels": [
                "adventure", "outdoor", "fitness",
                "family-friendly", "solo", "fun", "exciting",
                "cultural", "educational"
            ]

        }
    }
    
    # Make the API request
    response = requests.post("https://api-inference.huggingface.co/models/facebook/bart-large-mnli", headers=headers, json=payload)
    
    # Check the status of the response
    if response.status_code == 200:
        try:
            output = response.json()  # Parse JSON response
            print("API Response Output:", output)  # Log the actual response
            
            # Extract labels and scores
            labels = output.get("labels", [])
            scores = output.get("scores", [])

            # Pair labels with their corresponding scores
            combined = [{"label": label, "score": score} for label, score in zip(labels, scores)]
            
            # Sort the combined list based on scores in descending order
            sorted_output = sorted(combined, key=lambda x: x["score"], reverse=True)

            # Filter labels based on a score threshold (e.g., 0.2)
            return [item["label"] for item in sorted_output if item["score"] > 0.15]

        except ValueError:
            print("Error parsing JSON response")
            return []
    else:
        print(f"API error: {response.status_code} - {response.text}")
        return []




def generate_image_caption(image_path):
    api_url = "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning"
    headers = {"Authorization": "Bearer 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"}

    # Log the image path
    print(f"Sending image at path: {image_path}")

    if not os.path.exists(image_path):
        print(f"Error: Image file does not exist at {image_path}")
        return None

    for attempt in range(5):  # Try up to 5 times
        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
            response = requests.post(api_url, headers=headers, data=img_data)

        if response.status_code == 200:
            caption = response.json()[0]["generated_text"]
            return caption
        elif response.status_code == 503:
            print(f"Model loading, retrying in {attempt + 1} seconds...")
            time.sleep(attempt + 1)  # Wait longer with each attempt
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    print("Failed to get a response after multiple attempts.")
    return None

def get_price_tag(price):
    if price < 20:
        return ["budget"]
    elif price < 50:
        return ["mid-range"]
    else:
        return ["premium"]


def generate_activity_tags(image_path, activity_name, price):
    image_tags = get_image_tags(image_path)
    text_tags = get_text_tags(activity_name)
    price_tag = get_price_tag(price)

    # Combine all tags and remove duplicates
    all_tags = list(set(image_tags + text_tags + price_tag))
    return all_tags


class Activite(models.Model):
    nom = models.CharField(max_length=255)  # Nom de l'activité
    adresse = models.CharField(max_length=255)  # Emplacement de l'activité
    cout = models.DecimalField(max_digits=10, decimal_places=2, help_text="Coût en euros")  # Coût de l'activité
    image = models.ImageField(upload_to='images/activites/', blank=True, null=True, help_text="Image de l'activité")  # Image de l'activité
    duree = models.CharField(max_length=50, help_text="Durée de l'activité")  # Durée de l'activité
    pax = models.IntegerField(default=1, help_text="Nombre de personnes")  # Nombre de personnes pour l'activité

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"

    def __str__(self):
        return self.nom

    @classmethod
    def get_activities_with_captions(cls):
        activities = cls.objects.all()
        for activity in activities:
            if activity.image:
                activity.caption = generate_image_caption(activity.image.path)
            else:
                activity.caption = "No image available."
        return activities