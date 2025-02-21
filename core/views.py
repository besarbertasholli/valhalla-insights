from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Character

def character_list(request):
    search_query = request.GET.get("q", "")

    if search_query:
        characters = Character.objects.filter(
            Q(name__icontains=search_query) |
            Q(actor__name__icontains=search_query)
        ).select_related("actor")
    else:
        characters = Character.objects.select_related("actor")

    return render(request, "characters/list.html", {"characters": characters})

def character_profile(request, slug):
    character = get_object_or_404(Character, slug=slug)
    return render(request, "characters/profile.html", {"character": character})
