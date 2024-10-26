from django.db import models

class Fournisseur(models.Model):
    TYPES_DE_SERVICE = [
        ('hotel', 'Hôtel'),
        ('compagnie_aerienne', 'Compagnie Aérienne'),
        ('activite', 'Activité'),
    ]

    nom = models.CharField(max_length=255)
    type_service = models.CharField(max_length=30, choices=TYPES_DE_SERVICE)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    evaluation = models.FloatField(default=0.0)  # Évaluation de 0 à 5

    def __str__(self):
        return self.nom
