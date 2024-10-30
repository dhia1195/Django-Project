from django.contrib import admin
from .models import TexteSource, TexteTraduit

@admin.register(TexteSource)
class TexteSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'langue_source', 'contenu', 'date_creation')
    search_fields = ('langue_source', 'contenu')
    list_filter = ('langue_source', 'date_creation')
    ordering = ('-date_creation',)
    date_hierarchy = 'date_creation'


@admin.register(TexteTraduit)
class TexteTraduitAdmin(admin.ModelAdmin):
    list_display = ('id', 'texte_source', 'langue_cible', 'texte_traduit', 'date_traduction')
    search_fields = ('langue_cible', 'texte_traduit')
    list_filter = ('langue_cible', 'date_traduction')
    ordering = ('-date_traduction',)
    date_hierarchy = 'date_traduction'
