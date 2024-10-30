from django.shortcuts import render

def front_view(request):
    return render(request, 'index.html')  # Remplacez 'index.html' par le nom de votre fichier de template
