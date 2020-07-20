# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.test_db


    def __del__(self):
        self.client.close()


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            salary = item['salary']
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary(salary)
            del item['salary']
            collection = self.db[spider.name]
            collection.insert_one(item)
            return item

        if spider.name == 'sjru':
            print(item)
            collection = self.db[spider.name]
            collection.insert_one(item)
            return item

    def process_salary(self, salary):

        min_salary, max_salary, currency = None, None, None
        len_salary = len(salary)

        if len_salary == 1:
            return (min_salary, max_salary, currency)
        salary.pop()
        for i in range(len_salary - 1):
            if 'от' in salary[i]:
                min_salary = int(re.sub(r'[\.\s]', "", salary[i + 1]))
            if 'до' in salary[i]:
                max_salary = int(re.sub(r'[\.\s]', "", salary[i + 1]))
        currency = salary[len_salary - 2]
        return (min_salary, max_salary, currency)