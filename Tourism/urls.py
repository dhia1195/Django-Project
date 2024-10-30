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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reservations.views import front_view, get_image_for_destination  # Ensure both views are imported
from sentiment.views import sentiment_analysis_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('front/', front_view, name='front'),  # Ajoutez cette ligne pour votre vue
    path('get-image-for-destination/', get_image_for_destination, name='get_image_for_destination'),
    path('sentiment_analysis_view/', sentiment_analysis_view, name='sentiment_analysis'),  # Ajoutez cette ligne pour votre vue


]
if settings.DEBUG:  # Ensure this is only done in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)