# Generated by Django 4.2.19 on 2025-02-20 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='character',
            unique_together={('name', 'tv_series')},
        ),
    ]
