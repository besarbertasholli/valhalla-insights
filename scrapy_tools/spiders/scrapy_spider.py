import scrapy

class ScrapySpider(scrapy.Spider):

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
