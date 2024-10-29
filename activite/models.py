from django.db import models
import requests
import os
import base64
import time



API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def get_image_tags(image_path):
    with open(image_path, "rb") as image_file:
        img_data = base64.b64encode(image_file.read()).decode("utf-8")
        payload = {
            "parameters": {"candidate_labels": ["outdoor", "adventure", "relaxation", "sport", "water", "nature"]},
            "inputs": img_data
        }
        for attempt in range(5):
            response = requests.post(
                "https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                output = response.json()
                
                # Log the structure of `output` to understand it
                print("Received output from API:", output)
                
                # Adjust processing based on the response structure
                if isinstance(output, list):
                    return [item.get("label") for item in output if "label" in item]
                elif isinstance(output, dict) and "labels" in output:
                    return [label["label"] for label in output["labels"]]
                else:
                    print("Unexpected output format:", output)
                    return []

            elif response.status_code == 503:
                print(f"Model loading, retrying in {attempt + 1} seconds...")
                time.sleep(attempt + 1)
            else:
                print("Error:", response.json())
                return []

    print("Failed to get image tags after multiple attempts.")
    return []




def get_text_tags(activity_name):
    # Define your API URL and headers inside the function
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

    # Construct the input for the API
    payload = {
        "inputs": {
            "source_sentence": activity_name,
            "sentences": [
                "outdoor adventure", "nature activity", "relaxing experience", "extreme sports", "water activity"
            ]
        }
    }
    
    # Send the request to the API
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Check for successful response
    if response.status_code == 200:
        output = response.json()
        
        # Log the structure of `output` to understand it
        print("Received output from API for text tags:", output)
        
        # Adjust processing based on the response structure
        if isinstance(output, list) and all(isinstance(item, dict) for item in output):
            # Sort output by score if it is a list of dictionaries
            sorted_output = sorted(output, key=lambda x: x.get("score", 0), reverse=True)
            return [item["label"] for item in sorted_output if "label" in item]
        elif isinstance(output, list):
            # If it is a list of floats or other unexpected format, log it
            print("Unexpected list format in output:", output)
            return []
        else:
            print("Unexpected output format:", output)
            return []

    print("Error:", response.json())
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