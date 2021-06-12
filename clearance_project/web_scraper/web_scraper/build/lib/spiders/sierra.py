import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import json
import datetime

class SierraSpider(scrapy.Spider):
    name = "sierra"
    start_urls = [
        'https://www.sierra.com/clearance~1/men~d~5284',
 
    ]
    
    

    def parse(self, response):
        allowed_domains = 'https://www.sierra.com'
        for prod in response.css('div.productThumbnailContainer'):
            item = {}
            item['brand']= prod.css('a.productCard-title-brand-text::text').get().lstrip().rstrip()
            item['product_name']= prod.css('a.display-block::text').get().rstrip().lstrip()
            item['old_price']= prod.css('div.productPricing span.retailPrice::text').get().replace('Compare at $','')
            item['new_price']= prod.css('span.ourPrice::text').get().rstrip().lstrip().replace('$','')
            link = prod.css('a.display-block::attr(href)').get()
            image_link = 'https://www.sierra.com' + link
            item['link'] = image_link
            discount = (float(item['new_price'].replace('$','')) - float(item['old_price'].replace('$','')))/float(item['old_price'].replace('$',''))*100
            item['discount'] = str(discount)
            
            image = prod.css('a.js-productThumbnail::attr(href)').get()
            item['image'] = prod.css('img.productThumbnail::attr(src)').get()
                
            item['created_at'] = datetime.datetime.now().strftime(format='%Y-%m-%d %H:%m')

            yield Request(image_link, self.get_color_sizes, meta={'item':item})            
            
            # yield item
            
            next_page = response.css('div.productListingPagination.p-y.b-t.text-xs-center div a:nth-child(14)::attr(href)').get()
            if next_page is not None:
                url = allowed_domains + next_page
                yield response.follow(url, callback=self.parse)
                
    def get_color_sizes(self, response):
        item = response.meta['item']
        item['colors'] = ''
        item['sizes'] = ''
        if item['image'] == 'https://s.stpost.com/img/blank.gif':
            item['image'] = response.css('a.MagicZoom::attr(href)').get()
        yield item
    
        # def get_image(self, response):
        #     item = response.meta['item']
        # item['image'] = response.css('img.image-zoom__image::attr(src)').get()
        # yield item
        
    
