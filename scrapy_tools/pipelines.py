import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from core.models import Actor, Character


class VikingsPipeline:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def process_item(self, item, spider):
        print(f"Processing actor {item['actor_name']} with role {item['character_name']}")

        try:
            loop = asyncio.get_event_loop()

            actor, actor_created = await loop.run_in_executor(
                self.executor, 
                self.get_or_create_actor,
                item["actor_name"],
            )

            if actor_created:
                print(f"Created new actor: {actor.name}")

            character, character_created = await loop.run_in_executor(
                self.executor, 
                self.get_or_create_character,
                item["character_name"],
                actor,
                item["character_image_url"],
                item["character_description"]
            )

            if character_created:
                print(f"Created new character: {character.name}")
            else:
                needs_update = False
                if character.description != item["character_description"]:
                    character.description = item["character_description"]
                    needs_update = True
                
                if character.image_url != item["character_image_url"]:
                    character.image_url = item["character_image_url"]
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
        print(f"Processing actor {item['actor_name']} with role {item['character_name']}")

        try:
            loop = asyncio.get_event_loop()

            actor, actor_created = await loop.run_in_executor(
                self.executor,
                self.get_or_create_actor,
                item["actor_name"],
                item["actor_image_url"],
                item["actor_description"]
            )

            if actor_created:
                print(f"Created new actor: {actor.name}")
            else:
                needs_update = False
                if actor.image_url != item["actor_image_url"]:
                    actor.image_url = item["actor_image_url"]
                    needs_update = True

                if actor.description != item["actor_description"]:
                    actor.description = item["actor_description"]
                    needs_update = True

                if needs_update:
                    await loop.run_in_executor(self.executor, actor.save)
                    print(f"Updated actor: {actor.name}")

            character, character_created = await loop.run_in_executor(
                self.executor,
                self.get_or_create_character,
                item["character_name"],
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
    def process_item(self, item, spider):
        print(f"Processing player {item['name']}")

        print("Nothing is happening with this pipeline. Still needs to update.")

        return item
