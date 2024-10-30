from django.db import models

class TexteSource(models.Model):
    langue_source = models.CharField(
        max_length=50, 
        help_text="Langue du texte source (par exemple, 'fr' pour français)"
    )
    contenu = models.TextField(
        help_text="Contenu du texte à traduire"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.langue_source}: {self.contenu[:50]}"


class TexteTraduit(models.Model):
    texte_source = models.ForeignKey(
        TexteSource, 
        on_delete=models.CASCADE, 
        related_name="traductions"
    )
    langue_cible = models.CharField(
        max_length=50, 
        help_text="Langue cible de la traduction (par exemple, 'en' pour anglais)"
    )
    texte_traduit = models.TextField(
        help_text="Contenu du texte traduit"
    )
    date_traduction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.langue_cible}: {self.texte_traduit[:50]}"
        
