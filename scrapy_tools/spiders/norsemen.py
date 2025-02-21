import re
from .scrapy_spider import ScrapySpider
from scrapy_tools.items import NorsemenCharacterItem

class NorsemenSpider(ScrapySpider):
    name = "norsemen"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/title/tt5905354/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapy_tools.pipelines.NorsemenPipeline": 300,
        }
    }

    def parse(self, response):
        for cast in response.css('section[data-testid="title-cast"] div[data-testid="shoveler"] div[data-testid="shoveler-items-container"] div[data-testid="title-cast-item"]'):
            item = NorsemenCharacterItem()

            item["character_name"] = cast.css(".title-cast-item__characters-list ul li:first-child a[data-testid='cast-item-characters-link'] span::text").get(default="").strip()
            item["actor_name"] = cast.css("a[data-testid='title-cast-item__actor']::text").get(default="").strip()
            item["actor_image_url"] = cast.css("div[data-testid='title-cast-item__avatar'] .ipc-media--avatar img.ipc-image::attr(src)").get()

            details_url = cast.css("div[data-testid='title-cast-item__avatar'] .ipc-avatar a::attr(href)").get()
            if details_url:
                yield response.follow(
                    details_url,
                    callback=self.parse_cast,
                    errback=self.handle_parse_cast_failure,
                    meta={"item": item},
                    headers=response.request.headers
                )
            else:
                yield item

    def parse_cast(self, response):
        item = response.meta["item"]
        item["details_url"] = response.url
        item["actor_description"] = re.sub(r"\s+", " ", " ".join(
            response.css("section[data-testid='hero-parent'] .ipc-html-content-inner-div *::text").getall()
        ).strip())

        yield item


    def handle_parse_cast_failure(self, failure):
        """Handles failures in parse_cast and logs the error."""
        self.logger.warning(f"parse_cast failed: {failure.request.url}")

        if "item" in failure.request.meta:
            item = failure.request.meta["item"]
            item["details_url"] = failure.request.url
            item["description"] = ""
            yield item
