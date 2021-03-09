# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    allowed_domains = ['rozetka.com.ua']
    start_urls = ['https://rozetka.com.ua/notebooks/c80004/']

    def parse(self, response: Response):
        products = response.xpath("//li[contains(@class, 'catalog-grid__cell')]")[:20]

        for product in products:
            yield {
                'title': product.xpath(".//span[contains(@class, 'goods-tile__title')]/text()")[0].get(),
                'description': product.xpath(".//p[contains(@class, 'goods-tile__description_type_text')]/text()")[0].get(),
                'price': product.xpath(".//span[contains(@class, 'goods-tile__price-value')]/text()")[0].get()
                         + product.xpath(".//span[contains(@class, 'goods-tile__price-currency')]/text()")[0].get()
            }
