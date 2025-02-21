from django.contrib import admin
from .models import Actor, Character, Player

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "image_url", "description")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "actor", "tv_series")
    search_fields = ("name", "actor__name")
    list_filter = ("tv_series",)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "college")
    search_fields = ("name",)
    list_filter = ("position", "college",)
