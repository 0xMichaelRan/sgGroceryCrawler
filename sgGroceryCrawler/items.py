# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SggrocerycrawlerItem(scrapy.Item):
    
    title = scrapy.Field()
    brand = scrapy.Field()
    quantity = scrapy.Field()
    unit = scrapy.Field()
    # these 4 fields are extracted using (maybe) NLP algo
    
    small_img = scrapy.Field()
    large_img = scrapy.Field()
    # must have small_img
    
    now_price = scrapy.Field()
    old_price = scrapy.Field()
    promo = scrapy.Field()
    # must have now_price
    # promo may be removed (cuz there's no use)
    
    prd_url  = scrapy.Field()
    prd_code = scrapy.Field()
    # these 2 fields are optional, many site dont have product url
    
    # the following info is not crawled, but set by developer
    merchant = scrapy.Field()
    website = scrapy.Field()
    update_time = scrapy.Field()
    key = scrapy.Field()
    # key is brand + title + merchant
    # key is always small letter and used for search
