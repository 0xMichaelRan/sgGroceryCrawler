import pymongo
import datetime
import time
import re

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SggrocerycrawlerPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):

        # if product title is empty, discard
    	if not item or len(item['title']) == 0:
    		raise DropItem("Missing title, %s" % item)
        
        # if is a valid item, then we process the string data
        array = ['title', 'brand', 'quantity', 'unit', 
                'small_img', 'large_img', 
                'now_price', 'old_price', 'promo', 
                'prd_url', 'prd_code']
        
        # for each property of the item, remove all special chars
        for prop in array:
            if prop not in item or len(item[prop]) == 0:
                item[prop] = ""
            else:
                item[prop] = (item[prop].encode("utf-8")
                                .replace("\r", "")
                                .replace("\t", "")
                                .replace("\n", "")
                                .strip()
                             )
        
        # replace any S$ or $ sign from the price property
        item['old_price'] = item['old_price'].replace("S$", "").replace("$", "")
        item['now_price'] = item['now_price'].replace("S$", "").replace("$", "")

        # set current timestamp 
        ts = time.time()
        item['update_time'] = (datetime.datetime.fromtimestamp(ts)
            .strftime('%Y-%m-%d %H:%M:%S'))

        # key is brand + title + merchant
        item['key'] = (item['brand'].lower() + ' ' + item['title'].lower() + 
                       ' ' + item['merchant'].lower())
        
        # replace special chars in either end of title and brand
        # eg. some brand is '*' and some title ends with '#'
        item['title'] = re.sub(r"^\W+", "", item['title'])
        item['title'] = re.sub(r"\W+$", "", item['title'])

        item['brand'] = re.sub(r"^\W+", "", item['brand'])
        item['brand'] = re.sub(r"\W+$", "", item['brand'])


        # put the item into mongo db (using 'title' as key)
        self.collection.update(
            {'key': item['key']},
            dict(item), upsert=True
        )
        # The dict() constructs from sequences of key-value pairs
        # MongoDB upsert: update if it is already exist, or insert otherwise.

        # last step, print a msg in console
        log.msg("Grocery item added to MongoDB database!",
                level=log.DEBUG, spider=spider)

        return item
