# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose





class WebScraperItem(Item):
    product_name = Field()
    old_price = Field()
    new_price = Field()
    image = Field()
    link = Field()
    discount = Field()
    brand = Field()
    colors = Field()
    sizes = Field()
    created_at = Field()
    