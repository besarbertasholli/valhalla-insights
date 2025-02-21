from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

class Actor(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, related_name="characters")
    tv_series = models.CharField(
        max_length=50,
        choices=[("Vikings", "Vikings"), ("Norsemen", "Norsemen")],
        db_index=True,
    )
    search_vector = SearchVectorField(null=True)

    class Meta:
        unique_together = ("name", "tv_series")
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self):
        return f"{self.name}({self.actor.name}) of {self.tv_series}"
