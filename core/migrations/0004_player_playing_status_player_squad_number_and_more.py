# Generated by Django 4.2.19 on 2025-02-23 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_character_core_charac_search__b059e5_gin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='playing_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='squad_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
