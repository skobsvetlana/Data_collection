# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

class LeroymerlinRuItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    unit = scrapy.Field()
    specifications = scrapy.Field()
    specifications_name = scrapy.Field()
    specifications_value = scrapy.Field()





