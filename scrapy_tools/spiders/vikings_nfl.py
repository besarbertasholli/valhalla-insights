import scrapy
from scrapy_tools.items import VikingsPlayerItem


class VikingsNFLSpider(scrapy.Spider):
    name = "vikings_nfl"
    allowed_domains = ["vikings.com"]
    start_urls = ["https://www.vikings.com/team/players-roster/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapy_tools.pipelines.VikingsNFLPipeline": 300,
        }
    }

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.vikings.com/",
            "DNT": "1",  # Do Not Track
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)


    def parse(self, response):
        print("------------------------------------------")
        print(response.xpath("//body").get())
        yield {"test": "This is a test item"}
        # for player in response.css(".nfl-o-roster table tbody tr"):
        #     item = VikingsPlayerItem()
        #     print(player)

        #     item["name"] = player.css(".sorter-lastname .nfl-o-roster__player-name a::text").get(default="").strip()

        #     yield item
        
