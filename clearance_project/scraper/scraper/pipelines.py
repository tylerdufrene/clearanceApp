import pymongo
from itemadapter import ItemAdapter
import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from .settings import DB_CREDS

class MongoPipeline:

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
    


class MySQLPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(DB_CREDS['host'], DB_CREDS['user'], DB_CREDS['password'], 
                                    DB_CREDS['db'], charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO store_products (product_name, old_price, new_price, image, link, brand, discount, colors, sizes, created_at)  
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                       (item['product_name'].encode('utf-8'), 
                        item['old_price'].encode('utf-8'),
                        item['new_price'].encode('utf-8'),
                        item['image'].encode('utf-8'),
                        item['link'].encode('utf-8'),
                        item['brand'].encode('utf-8'),
                        item['discount'].encode('utf-8'),
                        item['colors'].encode('utf-8'),
                        item['sizes'].encode('utf-8'),
                        item['created_at'].encode('utf-8')))      
            self.conn.commit()   
        except MySQLdb.Error as e:
            print(e)
        return item
    
