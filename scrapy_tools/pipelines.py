import json
import asyncio
from django.db import transaction
from concurrent.futures import ThreadPoolExecutor
from core.models import Actor, Character, Player, SeasonStats


class VikingsPipeline:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def process_item(self, item, spider):
        print(f"Processing actor {item.get('actor_name')} with role {item.get('character_name')}")

        try:
            loop = asyncio.get_event_loop()

            actor, actor_created = await loop.run_in_executor(
                self.executor, 
                self.get_or_create_actor,
                item.get("actor_name"),
            )

            if actor_created:
                print(f"Created new actor: {actor.name}")

            character, character_created = await loop.run_in_executor(
                self.executor, 
                self.get_or_create_character,
                item.get("character_name"),
                actor,
                item.get("character_image_url"),
                item.get("character_description"),
            )

            if character_created:
                print(f"Created new character: {character.name}")
            else:
                needs_update = False
                if character.description != item.get("character_description"):
                    character.description = item.get("character_description")
                    needs_update = True
                
                if character.image_url != item.get("character_image_url"):
                    character.image_url = item.get("character_image_url")
                    needs_update = True

                if needs_update:
                    await loop.run_in_executor(self.executor, character.save)
                    print(f"Updated character: {character.name}")

        except Exception as e:
            spider.logger.error(f"Database error: {e}")

        return item

    def get_or_create_actor(self, name):
        """ Helper function to safely perform Django ORM operations. """
        obj, created = Actor.objects.get_or_create(
            name=name
        )
        return obj, created

    def get_or_create_character(self, name, actor, image_url, description):
        """ Helper function to safely perform Django ORM operations for Character. """
        obj, created = Character.objects.get_or_create(
            name=name,
            actor=actor,
            tv_series="Vikings",
            defaults={"image_url": image_url, "description": description}
        )
        return obj, created


class NorsemenPipeline:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def process_item(self, item, spider):
        print(f"Processing actor {item.get('actor_name')} with role {item.get('character_name')}")

        try:
            loop = asyncio.get_event_loop()

            actor, actor_created = await loop.run_in_executor(
                self.executor,
                self.get_or_create_actor,
                item.get("actor_name"),
                item.get("actor_image_url"),
                item.get("actor_description"),
            )

            if actor_created:
                print(f"Created new actor: {actor.name}")
            else:
                needs_update = False
                if actor.image_url != item.get("actor_image_url"):
                    actor.image_url = item.get("actor_image_url")
                    needs_update = True

                if actor.description != item.get("actor_description"):
                    actor.description = item.get("actor_description")
                    needs_update = True

                if needs_update:
                    await loop.run_in_executor(self.executor, actor.save)
                    print(f"Updated actor: {actor.name}")

            character, character_created = await loop.run_in_executor(
                self.executor,
                self.get_or_create_character,
                item.get('character_name'),
                actor,
            )

            if character_created:
                print(f"Created new character: {character.name}")

        except Exception as e:
            spider.logger.error(f"Database error: {e}")

        return item

    def get_or_create_actor(self, name, image_url, description):
        """Helper function to safely perform Django ORM operations for Actor."""
        obj, created = Actor.objects.get_or_create(
            name=name,
            defaults={"image_url": image_url, "description": description}
        )
        return obj, created

    def get_or_create_character(self, name, actor):
        """Helper function to safely perform Django ORM operations for Character."""
        obj, created = Character.objects.get_or_create(
            name=name,
            actor=actor,
            tv_series="Norsemen",
        )
        return obj, created


class VikingsNFLPipeline:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)

    async def process_item(self, item, spider):
        print(f"Processing player {item.get('name')}")
        
        try:
            loop = asyncio.get_event_loop()

            player, player_created = await loop.run_in_executor(
                self.executor, 
                self.get_or_create_player,
                item,
            )
            if player_created:
                print(f"Created new player: {player.name}")
            else:
                print(f"Player {player.name} exists. Skipped creating!")

            if "season_stats" in item:
                season_stats, season_stats_created = await loop.run_in_executor(
                    self.executor,
                    self.get_or_create_season_stats,
                    player,
                    item
                )
                if season_stats_created:
                    print(f"Created new player season stats for: {player.name}")
                else:
                    print(f"Player {player.name} season stats exist. Skipped creating!")

        except Exception as e:
            spider.logger.error(f"Database error: {e}")

        return item

    def get_or_create_player(self, item):
        """ Helper function to safely perform Django ORM operations for Player. """
        with transaction.atomic():
            player, created = Player.objects.update_or_create(
                name=item.get("name"),
                defaults={
                    "squad_number": item.get("squad_number"),
                    "position": item.get("position"),
                    "height": item.get("height"),
                    "weight": item.get("weight"),
                    "age": item.get("age"),
                    "years_experience": item.get("years_experience"),
                    "college": item.get("college"),
                    "bio": item.get("bio"),
                    "image_url": item.get("image_url"),
                }
            )
        return player, created

    def get_or_create_season_stats(self, player, item):
        """ Helper function to safely perform Django ORM operations for SeasonStats. """
        season_stats = item.get("season_stats", {})

        if not season_stats:  
            return None, False

        with transaction.atomic():
            season_stats_obj, created = SeasonStats.objects.update_or_create(
                player=player,
                season=season_stats.get("season"),
                defaults={
                    "team": season_stats.get("team", "Minnesota Vikings"),
                    "games_played": season_stats.get("games_played"),
                    "games_started": season_stats.get("games_started"),
                    "rushing_attempts": season_stats.get("rushing_attempts"),
                    "rushing_yards": season_stats.get("rushing_yards"),
                    "rushing_average": season_stats.get("rushing_average"),
                    "rushing_touchdowns": season_stats.get("rushing_touchdowns"),
                    "receptions": season_stats.get("receptions"),
                    "receiving_yards": season_stats.get("receiving_yards"),
                    "receiving_average": season_stats.get("receiving_average"),
                    "longest_reception": season_stats.get("longest_reception"),
                    "receiving_touchdowns": season_stats.get("receiving_touchdowns"),
                    "fumbles": season_stats.get("fumbles"),
                    "fumbles_lost": season_stats.get("fumbles_lost"),
                }
            )

        return season_stats_obj, created
