from django.db import models

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