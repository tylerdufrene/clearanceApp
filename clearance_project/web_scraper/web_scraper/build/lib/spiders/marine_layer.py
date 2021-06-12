import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
import json
import datetime


class MarineLayerSpider(scrapy.Spider):
    name = "marine_layer"
    start_urls = [
        'https://www.marinelayer.com/collections/guys-last-call',
 
    ]
    
    

    def parse(self, response):
        
        for prod in response.css('div.grid__item div.grid__item'):
            item = {}
            item['brand']= 'Marine Layer'
            item['product_name']= prod.css('div.medium-down--show h6.product-info__name::text').get().lstrip().rstrip()
            item['old_price']= prod.css('span.ComparePrice::text').get().replace('$','').replace(',','')
            item['new_price']= prod.css("h6.product-info__name div.product-info__price span:nth-child(3)::text").get().replace('$','').replace(',','')
            link = prod.css('a.grid__image::attr(href)').get()
            image_link = 'https://www.marinelayer.com' + link
            item['link'] = image_link
            discount = (float(item['new_price']) - float(item['old_price']))/float(item['old_price'])*100
            item['discount'] = str(discount)
            item['created_at'] = datetime.datetime.now().strftime(format='%Y-%m-%d %H:%m')

            
            if item['product_name']=='':
                prod_name = item['link'].split('/')[-1]
                prod_name1 = prod_name.replace('-',' ').title()
                item['product_name'] = prod_name1
                
            item['image'] = prod.css('img.product-photo::attr(src)').get()
                
            yield Request(image_link, self.get_color_sizes, meta={'item':item})            
            
            # yield item
            
            # next_page = response.css('li.pagination__item--next a::attr(href)').get()
            # if next_page is not None:
            #     url = allowed_domains[0] + next_page
            #     yield response.follow(url, callback=self.parse)
                
    def get_color_sizes(self, response):
        item = response.meta['item']
        colors = response.css('div.grid--full div.color-variant-container img::attr(src)').extract()
        item['colors'] = json.dumps(colors)
        sizes = response.css('div.grid--full div.size-variant-container ul.inline-list li::attr(class)').extract()
        item['sizes'] = json.dumps(sizes)
        yield item
    
    
    
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MarineLayerSpider)
    process.start()