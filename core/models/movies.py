from django.db import models
from django.utils.text import slugify

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
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ("name", "tv_series")

    def __str__(self):
        if self.actor:
            return f"{self.name}({self.actor.name}) of {self.tv_series}"
        else:
            return f"{self.name} of {self.tv_series}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.tv_series}")
            self.slug = base_slug

            count = 1
            while Character.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)
