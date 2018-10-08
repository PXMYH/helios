# -*- coding: utf-8 -*-
import scrapy


class CraigbotSpider(scrapy.Spider):
    name = 'craigbot'
    allowed_domains = ['craigslist.ca']
    start_urls = ['https://vancouver.craigslist.ca/search/apa']

    def parse(self, response):
        print ("parsing the response {0}".format(response.body))
        listings = response.xpath('//p[@class="result-info"]')
        print ("\n*************\nlistings: {0}".format(listings))
        for listing in listings:
            # title = listing.xpath('.//a[@class="result-title hdrlnk"]/text().extract()')
            title = listing.xpath('a/text()').extract_first()
            price = listing.xpath('span[@class="result-price"]/text()').extract()
            area = listing.xpath('span[@class="housing"]/text()').extract()
            yield {'Title': title, 'Price': price, 'Area': area}
