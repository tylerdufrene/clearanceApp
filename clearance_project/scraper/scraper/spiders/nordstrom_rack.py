import scrapy
import base64
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import json
import datetime

from ..items import WebScraperItem


class NordstromRackSpider(scrapy.Spider):
    name = "nordstrom_rack"
    allowed_domains = ['nordstromrack.com']
    start_urls = [
        'https://www.nordstromrack.com/clearance/Men/Clothing?page=1&sort=most_popular',
 
    ]
    

    

    def parse(self, response):
        allowed_domains = ['https://www.nordstromrack.com']
        
        for prod in response.css('article._1AOd3'):
            item = WebScraperItem()
            item['brand']= prod.css('div._3EXU6::text').get()
            item['product_name']= prod.css('a._3TDAp::text').get()
            if prod.css('div._1jexH::text').get() is None:
                continue
            elif '-' in prod.css('div._1jexH::text').get():
                item['old_price'] = prod.css('div._1jexH::text').get().split(' ')[0].replace('$','').replace(',','')
            else:
                item['old_price']= prod.css('div._1jexH::text').get().replace('$','').replace(',','')
            item['new_price']= prod.css('div._1eA2_::text').get().split(' ')[0].replace('$','')
            item['link']= 'https://www.nordstromrack.com' + prod.css('a._1av3_::attr(href)').get()
            image_link = 'https://www.nordstromrack.com' + item['link']
            discount = (float(item['new_price'].replace('$','')) - float(item['old_price'].replace('$','')))/float(item['old_price'].replace('$',''))*100
            item['discount'] = str(discount)
            item['created_at'] = datetime.datetime.now().strftime(format='%Y-%m-%d %H:%m')
            item['image'] = prod.css('img.TDd9E::attr(src)').get()
            item['sizes'] = ''
            item['colors'] = ''
            # yield Request(image_link, self.get_image, meta={'item':item})                
            
            
            
            next_page = response.css('li._1ZIyZ a._2WIqd::attr(href)')[-1].get()
            if next_page is not None:
                url = 'https://www.nordstromrack.com/clearance/Men/Clothing' + next_page
                yield response.follow(url, callback=self.parse)
                
            yield item
                
    # def get_image(self, response):
    #     item = response.meta['item']
    #     # item['image'] = response.css('img.HYpZP::attr(src)').get()

    #     yield item


# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(NordstromRackSpider)
#     process.start()