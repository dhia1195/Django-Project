"""
URL configuration for Tourism project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from reservations.views import front_view, get_image_for_destination, get_reservations  
from traductions.views import translation_view,get_translations
from reservations import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('front/', front_view, name='front'),  # Route for the main view
    path('get-image-for-destination/', get_image_for_destination, name='get_image_for_destination'),  # Route for image generation
    path('translation_view/', translation_view, name='translation'),  # Route for image generation
 path('translation/', get_translations, name='translationt'),  # Route for image generation

    
    # path('get-reclamationt/', get_reclamationt, name='get_reclamationt'),

    path('get-reservations/', get_reservations, name='get_reservations'),  # Route for fetching reservations
    path('delete-reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),


]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
