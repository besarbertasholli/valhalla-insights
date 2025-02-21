import scrapy

class ScrapySpider(scrapy.Spider):

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
