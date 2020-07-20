import scrapy
from scrapy.http import HtmlResponse
from lesson6.jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&st=searchVacancy&fromSearch=true&text=python']

    def parse(self, response:HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()

        vacancy_links = response.css('a.bloko-link.HH-LinkModifier::attr(href)').extract()

        for vac_link in vacancy_links:
            yield response.follow(vac_link, callback=self.vacancy_parse)

        yield response.follow(next_page, callback=self.parse)


    def vacancy_parse(self, response:HtmlResponse):
        vac_name = response.css('h1::text').extract_first()
        vac_employer_name = response.xpath("//span[@class='bloko-section-header-2 bloko-section-header-2_lite']/text()").extract()[-1]
        vac_city = response.xpath("//p[@data-qa='vacancy-view-location']/text()").extract_first()
        vac_link = response.url
        vac_sourse = self.name
        vac_salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        yield JobparserItem(vacancy_name=vac_name, employer_name=vac_employer_name, salary=vac_salary,
                            link=vac_link, city=vac_city, sourse=vac_sourse)

