# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import os
from urllib.parse import urlparse
import re


class DataBasePipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.avito_photos


    def __del__(self):
        self.client.close()


    def process_item(self, item, spider):
        item['price'] = self.process_price(item['price'], item['currency'], item['unit'])
        item['description'] = self.process_description(item['description'], item['name'])
        item['specifications'] = self.process_specifications(item['specifications_name'], item['specifications_value'])
        del item['currency']
        del item['unit']
        del item['specifications_name']
        del item['specifications_value']
        collection = self.db[spider.name]
        collection.insert_one(item)
        return item


    def process_price(self, price, currency, unit):
        price_1 = f'{price[0]} {currency[0]}/{unit[0]}'
        price_2 = f'{price[1]} {currency[1]}/{unit[1]}'
        return (price_1, price_2)


    def process_description(self, description, name):
        description = ' '.join(description)
        return f'{name}{description}'


    def process_specifications(self, name, value):
        specifications = {}
        lenth = len(name)
        for i in range(lenth):
            value[i] = re.sub('\s', '', value[i])
            specifications[name[i]] = value[i]
        return specifications


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta=item)
                except Exception as e:
                    print(e)


    def file_path(self, request, response=None, info=None):
        file_name = os.path.basename(urlparse(request.url).path)
        path = request.meta['url'][0].split('/')[-2]
        path = path.replace('-', '_') + '/'
        path = 'images/' + path + file_name
        return path


    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item



