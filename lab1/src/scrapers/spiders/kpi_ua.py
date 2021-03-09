# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class KpiUaSpider(scrapy.Spider):
    name = 'kpi_ua'
    start_urls = ['https://kpi.ua/']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@src[starts-with(., 'http')]")
        all_text = response.xpath(
            "//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()")

        yield {
            'url': response.url,
            'payload': [{'type': 'text', 'data': text.get().strip()} for text in all_text] +
                       [{'type': 'image', 'data': image.get()} for image in all_images]
        }

        if response.url == self.start_urls[0]:
            link_elems = response.xpath("//a/@href[starts-with(., 'https://kpi.ua/') or starts-with(., '/')]")
            links = [link.get() for link in link_elems if link.get() != "https://kpi.ua/"][:19]
            for l in links:
                link = 'https://kpi.ua/' + l
                yield scrapy.Request(link, self.parse)