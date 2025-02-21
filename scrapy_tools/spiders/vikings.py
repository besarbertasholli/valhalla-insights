from .scrapy_spider import ScrapySpider
from scrapy_tools.items import VikingsCharacterItem

class VikingsSpider(ScrapySpider):
    name = "vikings"
    allowed_domains = ["history.com", "history.de"]
    start_urls = ["https://www.history.com/shows/vikings/cast"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapy_tools.pipelines.VikingsPipeline": 300,
        }
    }

    def parse(self, response):
        for character in response.css("div.tile-list.tile-boxed ul li"):
            item = VikingsCharacterItem()

            item["character_name"] = character.css(".details strong::text").get(default="").strip()
            item["actor_name"] = character.css(".details small::text").get(default="").replace("Played by", "").strip()
            item["character_image_url"] = character.css(".img-container img::attr(src)").get()

            details_url = character.css("a::attr(href)").get()
            if details_url:
                yield response.follow(
                    details_url,
                    callback=self.parse_character,
                    errback=self.handle_parse_character_failure,
                    meta={"item": item},
                    headers=response.request.headers
                )
            else:
                yield item

    def parse_character(self, response):
        item = response.meta["item"]
        item["details_url"] = response.url

        description_element = response.css(".main-article .section-title + *")
        if description_element and description_element.xpath("name()").get() == "p":
            item["character_description"] = " ".join(description_element.css("::text").getall()).strip()
        elif description_element and description_element.xpath("name()").get() == "div":
            item["character_description"] = " ".join(description_element.css("p::text").getall()).strip()
        else:
            item["character_description"] = ""

        item["actor_id"] = None
        yield item

    def handle_parse_character_failure(self, failure):
        """Handles failures in parse_character and logs the error."""
        self.logger.warning(f"parse_character failed: {failure.request.url}")

        if "item" in failure.request.meta:
            item = failure.request.meta["item"]
            item["details_url"] = failure.request.url
            item["description"] = ""
            yield item