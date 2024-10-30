from django.db import models

class Avis(models.Model):
    utilisateur = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    commentaire = models.TextField()
    note = models.PositiveIntegerField()  # Une note entre 0 et 5, par exemple
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.utilisateur} sur {self.destination} ({self.note}/5)"


class AnalyseSentiment(models.Model):
    avis = models.OneToOneField(Avis, on_delete=models.CASCADE)  # Lié à un avis spécifique
    sentiment = models.CharField(max_length=50)
    score = models.FloatField()  # Score numérique du sentiment (ex: -1 à 1)
    date_analyse = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analyse : {self.sentiment} (Score: {self.score})"

