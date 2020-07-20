from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson7.avitoparser import settings
from lesson7.avitoparser.spiders.avitoru import AvitoruSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoruSpider, search='Mercedes gle coupe', city='izhevsk')
    process.start()

