from django.db import models
from django.utils.text import slugify

class Player(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    team = models.CharField(max_length=100, default="Minnesota Vikings")
    squad_number = models.PositiveIntegerField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=50, blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)  # lbs
    age = models.PositiveIntegerField(blank=True, null=True)
    years_experience = models.CharField(max_length=50, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)
    playing_status = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.position})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.position}")
            self.slug = base_slug

            count = 1
            while Player.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{count}"
                count += 1
        super().save(*args, **kwargs)


class SeasonStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="season_stats")
    season = models.IntegerField()  # Year
    team = models.CharField(max_length=100, default="Minnesota Vikings")

    # Player performance stats
    games_played = models.PositiveIntegerField(blank=True, null=True)  # G
    games_started = models.PositiveIntegerField(blank=True, null=True)  # GS
    rushing_attempts = models.PositiveIntegerField(blank=True, null=True)  # ATT
    rushing_yards = models.PositiveIntegerField(blank=True, null=True)  # YDS
    rushing_average = models.FloatField(blank=True, null=True)  # AVG
    rushing_touchdowns = models.PositiveIntegerField(blank=True, null=True)  # TD
    receptions = models.PositiveIntegerField(blank=True, null=True)  # REC
    receiving_yards = models.PositiveIntegerField(blank=True, null=True)  # YDS
    receiving_average = models.FloatField(blank=True, null=True)  # AVG
    longest_reception = models.PositiveIntegerField(blank=True, null=True)  # LNG
    receiving_touchdowns = models.PositiveIntegerField(blank=True, null=True)  # TD
    fumbles = models.PositiveIntegerField(blank=True, null=True)  # FUM
    fumbles_lost = models.PositiveIntegerField(blank=True, null=True)  # LOST

    class Meta:
        unique_together = ("player", "season")

    def __str__(self):
        return f"{self.player.name} - {self.season}"
