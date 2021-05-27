import scrapy

from web_scraper.items import WebScraperItem


class HowlerBrosSpider(scrapy.Spider):
    name = "howler_bros"

    start_urls = [
            'https://howlerbros.com/collections/last-call',
        ]

    def parse(self, response):
        for product in response.css('h2.grid-product'):
            item = WebScraperItem()
            item['product_name'] = product.css('span.grid-name::text').get()
            item['old_price'] = product.css('span.grid-strike::text').get()
            item['new_price'] = product.css('span.grid-onsale::text').get()
            item['image'] = product.css('img.primary').xpath('@data-srcset').get()
            item['link'] = product.css('h2.grid-product a::attr(href)').get()
            
            yield item