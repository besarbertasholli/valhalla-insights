import scrapy
from scrapy_tools.items import VikingsPlayerItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse


class VikingsNFLSpider(scrapy.Spider):
    name = "vikings_nfl"
    allowed_domains = ["vikings.com"]
    start_urls = ["https://www.vikings.com/team/players-roster/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapy_tools.pipelines.VikingsNFLPipeline": 300,
        }
    }

    def parse(self, response):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(response.url)
        page_source = driver.page_source
        driver.quit()

        response = HtmlResponse(url=response.url, body=page_source, encoding="utf-8", request=response.request)

        for player in response.css(".nfl-o-roster table tbody tr"):
            item = VikingsPlayerItem()
            item["image_url"] = player.css(".sorter-lastname .d3-o-media-object__figure picture .img-responsive::attr(src)").get().replace("t_lazy/", "")
            item["name"] = player.css(".sorter-lastname .nfl-o-roster__player-name a::text").get()
            item["squad_number"] = player.css(".sorter-lastname + td::text").get()
            item["position"] = player.css("td:nth-child(3)::text").get()
            item["height"] = player.css(".sorter-custom-height::text").get()
            item["weight"] = player.css(".sorter-custom-height + td::text").get()
            item["age"] = age if (age := player.css("td:nth-child(6)::text").get()) and age.strip() != "N/A" else None
            item["years_experience"] = player.css("td:nth-child(7) span::text").get()
            item["college"] = player.css("td:nth-child(8)::text").get()

            details_url = player.css(".sorter-lastname .nfl-o-roster__player-name a::attr(href)").get()

            if details_url:
                yield response.follow(
                    details_url,
                    callback=self.parse_player,
                    errback=self.handle_parse_player_failure,
                    meta={"item": item},
                    headers=response.request.headers
                )
            else:
                yield item

    def parse_player(self, response):
        item = response.meta["item"]
        item["details_url"] = response.url

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(response.url)
        page_source = driver.page_source
        driver.quit()

        response = HtmlResponse(url=response.url, body=page_source, encoding="utf-8")

        item["bio"] = response.css(".nfl-c-biography .nfl-c-body-part:nth-child(2) ul li::text").getall()

        for player_stats in response.css(".nfl-t-stats--table table[summary='Career Stats'] tbody tr"):
            season = player_stats.css("td:first-child::text").get()

            if season and season.strip().isdigit() and int(season) == 2021:
                item["season_stats"] = {
                    "season": int(season),
                    "games_played": player_stats.css("td:nth-child(3)::text").get(),
                    "games_started": player_stats.css("td:nth-child(4)::text").get(),
                    "rushing_attempts": player_stats.css("td:nth-child(5)::text").get(),
                    "rushing_yards": player_stats.css("td:nth-child(6)::text").get(),
                    "rushing_average": player_stats.css("td:nth-child(7)::text").get(),
                    "rushing_touchdowns": player_stats.css("td:nth-child(8)::text").get(),
                    "receptions": player_stats.css("td:nth-child(9)::text").get(),
                    "receiving_yards": player_stats.css("td:nth-child(10)::text").get(),
                    "receiving_average": player_stats.css("td:nth-child(11)::text").get(),
                    "longest_reception": player_stats.css("td:nth-child(12)::text").get(),
                    "receiving_touchdowns": player_stats.css("td:nth-child(13)::text").get(),
                    "fumbles": player_stats.css("td:nth-child(14)::text").get(),
                    "fumbles_lost": player_stats.css("td:nth-child(15)::text").get(),
                }

                team_that_season = player_stats.css("td:nth-child(2)::text").get()
                if team_that_season and team_that_season.strip() != "Minnesota Vikings":
                    item["season_stats"]["team"] = team_that_season.strip()

        yield item

    def handle_parse_player_failure(self, failure):
        """Handles failures in parse_player and logs the error."""
        self.logger.warning(f"parse_player failed: {failure.request.url}")

        if "item" in failure.request.meta:
            item = failure.request.meta["item"]
            item["details_url"] = failure.request.url
            item["description"] = ""
            yield item
