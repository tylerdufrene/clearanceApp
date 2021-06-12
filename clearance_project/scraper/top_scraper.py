import os 


import MySQLdb
from scraper.settings import DB_CREDS



MySQLdb.connect(DB_CREDS['host'], DB_CREDS['user'], DB_CREDS['password'], 
                                    DB_CREDS['db'], charset="utf8",
                                    use_unicode=True)

# cursor= db.cursor()

# cursor.execute("TRUNCATE TABLE table_name")

# db.close()

os.system("scrapy crawl sierra")
os.system("scrapy crawl howler_bros")
os.system('scrapy crawl nordstrom_rack')
os.system('scrapy crawl marine_layer')
