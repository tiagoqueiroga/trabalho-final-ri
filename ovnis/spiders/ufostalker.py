# -*- coding: utf-8 -*-
import scrapy


class UfostalkerSpider(scrapy.Spider):
    name = 'ufostalker'
    allowed_domains = ['http://www.ufostalker.com']
    start_urls = ['http://http://www.ufostalker.com/']

    def parse(self, response):
        pass
