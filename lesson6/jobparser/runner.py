from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson6.jobparser import settings
from lesson6.jobparser.spiders.hhru import HhruSpider
from lesson6.jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()

