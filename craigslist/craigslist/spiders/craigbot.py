# -*- coding: utf-8 -*-
import scrapy


class CraigbotSpider(scrapy.Spider):
    name = 'craigbot'
    allowed_domains = ['craigslist.ca']
    start_urls = ['https://vancouver.craigslist.ca/search/apa']

    def parse(self, response):
        print ("parsing the response {0}".format(response.body))
        titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        print ("titles: {0}".format(titles))
        for title in titles:
            yield {'Title': title}
        # yield scraped_info
