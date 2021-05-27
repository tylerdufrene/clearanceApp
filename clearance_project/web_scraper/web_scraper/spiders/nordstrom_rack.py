import scrapy
import base64
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from web_scraper.items import WebScraperItem
from scrapy.http import Request
import json
import datetime


class NordstromRackSpider(scrapy.Spider):
    name = "nordstrom_rack"
    allowed_domains = ['nordstromrack.com']
    start_urls = [
        'https://www.nordstromrack.com/c/clearance/men?page=1&sort=most_popular',
 
    ]
    
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="pagination__item.pagination__item--next"]',)), callback="parse", follow= True),
    )
    
    

    def parse(self, response):
        allowed_domains = ['https://www.nordstromrack.com']
        
        for prod in response.css('div.product-grid-item'):
            item = WebScraperItem()
            item['brand']= prod.css('div.product-grid-item__brand::text').get()
            item['product_name']= prod.css('div.product-grid-item__title::text').get()
            item['old_price']= prod.css('del::text').get().replace('$','')
            item['new_price']= prod.css('span.product-grid-item__sale-price::text').get().replace('$','')
            link = prod.css('a.product-grid-item__details-container::attr(href)').get()
            image_link = allowed_domains[0] + link
            item['link'] = image_link
            discount = (float(item['new_price'].replace('$','')) - float(item['old_price'].replace('$','')))/float(item['old_price'].replace('$',''))*100
            item['discount'] = str(discount)
            item['created_at'] = datetime.datetime.now().strftime(format='%Y-%m-%d %H:%m')

            yield Request(image_link, self.get_image, meta={'item':item})                
            
            # yield item
            
            next_page = response.css('li.pagination__item--next a::attr(href)').get()
            if next_page is not None:
                url = allowed_domains[0] + next_page
                yield response.follow(url, callback=self.parse)
                
    def get_image(self, response):
        item = response.meta['item']
        item['image'] = response.css('img.image-zoom__image::attr(src)').get()
        sizes = response.css('div.product-page__details span.sku-item__text::text').extract()
        item['sizes'] = json.dumps(sizes)
        colors = response.css('div.product-page__details img.sku-item__swatch::attr(src)').extract()
        item['colors'] = json.dumps(colors)
        yield item
    