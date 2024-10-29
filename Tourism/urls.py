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
from reservations.views import front_view, get_image_for_destination, get_reservations  # Ensure both views are imported
from activite.views import generate_activity_tags_view
from user_client.views import signup_login_view,login,signup,logout_view
from .decorators import login_required,logout_required
from reservations import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('front/', login_required(front_view), name='front'),
    path('get-image-for-destination/', login_required(get_image_for_destination), name='get_image_for_destination'),
    path('auth/signup/', logout_required(signup), name='signup'),
    path('auth/login/', logout_required(login), name='login'),
    path('auth/logout/', login_required(logout_view), name='logout'),
    path('auth/', logout_required(signup_login_view), name='auth'),
    path('get-reservations/', login_required(get_reservations), name='get_reservations'),
    path('generate-activity-tags/', generate_activity_tags_view, name='generate_activity_tags'),
    path('delete-reservation/<int:reservation_id>/', login_required(views.delete_reservation), name='delete_reservation'),
    path('update-reservation/<int:reservation_id>/', login_required(views.update_reservation), name='update_reservation'),
   
]



# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
