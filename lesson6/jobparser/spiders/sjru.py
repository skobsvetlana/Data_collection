import scrapy
from scrapy.http import HtmlResponse
from lesson6.jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()

    #     vacancy_links = response.xpath("//a[@class='icMQ_ _6AfZ9 f-test-link-Python_developer _2JivQ _1UJAN']/@href").extract()
    #     print(next_page)
    #     print(vacancy_links)
    #
    #     for vac_link in vacancy_links:
    #         yield response.follow(vac_link, callback=self.vacancy_parse)
    #
    #     yield response.follow(next_page, callback=self.parse)
    #
    # def vacancy_parse(self, response:HtmlResponse):
    #     vac_name = response.xpath("//span[@class='_1rS-s']/text()").extract_first()
    #     vac_employer_name = None
    #     vac_city = response.xpath("//span[@class='_3mfro _1hP6a _2JVkc']/text()").extract_first()
    #     vac_link = response.url
    #     vac_sourse = self.name
    #     vac_salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
    #     yield JobparserItem(vacancy_name=vac_name, employer_name=vac_employer_name, salary=vac_salary,
    #                         link=vac_link, city=vac_city, sourse=vac_sourse)
