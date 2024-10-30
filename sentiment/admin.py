from django.contrib import admin

from django.contrib import admin
from .models import Avis, AnalyseSentiment

@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'destination', 'commentaire', 'note', 'date_creation')

@admin.register(AnalyseSentiment)
class AnalyseSentimentAdmin(admin.ModelAdmin):
    list_display = ('avis', 'sentiment', 'score', 'date_analyse')


