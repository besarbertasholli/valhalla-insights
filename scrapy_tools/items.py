import scrapy


class VikingsCharacterItem(scrapy.Item):
    character_name = scrapy.Field()
    actor_name = scrapy.Field()
    character_image_url = scrapy.Field()
    details_url = scrapy.Field()
    character_description = scrapy.Field()
    actor_id = scrapy.Field()


class NorsemenCharacterItem(scrapy.Item):
    character_name = scrapy.Field()
    actor_name = scrapy.Field()
    actor_image_url = scrapy.Field()
    details_url = scrapy.Field()
    actor_description = scrapy.Field()
