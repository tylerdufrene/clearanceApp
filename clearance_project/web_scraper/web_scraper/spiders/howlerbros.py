import scrapy
import MySQLdb

from web_scraper.items import WebScraperItem
from web_scraper.settings import DB_CREDS
from scrapy.http import Request
import json
import datetime

class HowlerBrosSpider(scrapy.Spider):
    name = "howler_bros"

    start_urls = [
            'https://howlerbros.com/collections/last-call',
        ]
    

    def parse(self, response):
        for product in response.css('h2.grid-product'):
            item = WebScraperItem()
            item['product_name'] = product.css('span.grid-name::text').get()
            item['old_price'] = product.css('span.grid-strike::text').re('\d+.*')[0]
            item['new_price'] = product.css('span.grid-onsale::text').re('\d+.*')[0]
            item['image'] = (product.css('img.primary').xpath('@data-srcset').get().replace('\n', '').replace('\t', '').replace('//','')
                             .replace('1000w','').replace('900w','').replace('800w','').replace('700w','').replace('600w','').replace('500w','')
                             .replace(',', ''))
            
            item['image'] = item['image'].split(' ')[0]
            
            link = product.css('h2.grid-product a::attr(href)').get()
            item['link'] = 'http://howlerbros.com' +link
            image_link = 'http://howlerbros.com' +link
            
            discount = (float(item['new_price']) - float(item['old_price']))/float(item['old_price'])*100
            item['discount'] = str(discount)
            item['brand'] = 'Howler Bros'
            item['created_at'] = datetime.datetime.now().strftime(format='%Y-%m-%d %H:%m')
            
            yield Request(image_link, self.get_color_sizes, meta={'item':item})            
            
            # yield item
            
            # next_page = response.css('li.pagination__item--next a::attr(href)').get()
            # if next_page is not None:
            #     url = allowed_domains[0] + next_page
            #     yield response.follow(url, callback=self.parse)
                
    def get_color_sizes(self, response):
        item = response.meta['item']
        colors = response.css('div#product-options img::attr(src)').extract()
        item['colors'] = json.dumps(colors)
        sizes = response.css('div.option-group div.swatch-element::attr(data-value)').extract()
        item['sizes'] = json.dumps(sizes)
        yield item