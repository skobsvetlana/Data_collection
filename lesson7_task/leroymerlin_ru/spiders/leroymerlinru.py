import scrapy
from scrapy.http import HtmlResponse
from lesson7_task.leroymerlin_ru.items import LeroymerlinRuItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/']

    def __init__(self, search, city):
        self.start_urls = [f'https://{city}.leroymerlin.ru/search/?q={search}']
        print(self.start_urls)


    def parse(self, response):
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a")

        ads_links = response.xpath("//div[@class='product-name']/a")
        for link in ads_links:

            prod_choices_links = response.xpath("//a[@class='image']")
            for choice in prod_choices_links:
                yield response.follow(choice, callback=self.parse_ads)

            yield response.follow(link, callback=self.parse_ads)

        yield response.follow(next_page, callback=self.parse)

    def parse_prod_choices(self, response):
        pass


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinRuItem(), response= response)
        loader.add_xpath('name', "//uc-pdp-card-ga-enriched[@class='card-data']/h1/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']//@src")
        loader.add_xpath('description', "//section[@id='nav-description']//p/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@slot='price']//text()")
        loader.add_xpath('currency', "//span[@slot='currency']//text()")
        loader.add_xpath('unit', "//span[@slot='unit']//text()")
        loader.add_xpath('specifications_name', "//div[@class='def-list__group']/dt/text()")
        loader.add_xpath('specifications_value', "//div[@class='def-list__group']/dd/text()")
        yield loader.load_item()



