from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import character_list, character_profile

urlpatterns = [
    path("", character_list, name="character_list_view"),
    path("characters/<slug:slug>/", character_profile, name="character_profile_view"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
