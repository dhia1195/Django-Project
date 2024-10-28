from django.db import models

class Activite(models.Model):
    nom = models.CharField(max_length=255)  # Nom de l'activité
    adresse = models.CharField(max_length=255)  # Emplacement de l'activité
    horaire = models.CharField(max_length=255, help_text="Horaires d'ouverture, par exemple: 09:00 - 18:00")  # Horaires d'ouverture
    cout = models.DecimalField(max_digits=10, decimal_places=2, help_text="Coût en euros")  # Coût de l'activité
    evaluation = models.FloatField(default=0.0)  # Évaluation de l'activité (0 à 5)
    image = models.ImageField(upload_to='images/activites/', blank=True, null=True, help_text="Image de l'activité")  # Image de l'activité



    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"

    def __str__(self):
        return self.nom