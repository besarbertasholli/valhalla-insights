from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render
from .models import Character

def characters_list(request):
    search_query = request.GET.get("q", "")

    if search_query:
        query = SearchQuery(search_query)
        characters = (
            Character.objects.annotate(
                rank=SearchRank(SearchVector("name", "description"), query)
            )
            .filter(search_vector=query)
            .select_related("actor")
            .order_by("-rank")
        )
    else:
        characters = Character.objects.select_related("actor")

    return render(request, "characters/list.html", {"characters": characters})
