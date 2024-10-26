from django.shortcuts import render

def front_view(request):
    # Your view logic here
    return render(request, 'index.html')
