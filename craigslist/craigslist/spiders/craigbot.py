# -*- coding: utf-8 -*-
import scrapy


class CraigbotSpider(scrapy.Spider):
    name = 'craigbot'
    allowed_domains = ['craigslist.ca']
    # start_urls = ['https://vancouver.craigslist.ca/search/apa']
    start_urls = ['https://vancouver.craigslist.ca/search/van/apa?min_bedrooms=2&max_bedrooms=2']

    def parse(self, response):
        print ("parsing the response {0}".format(response.body))
        listings = response.xpath('//p[@class="result-info"]')
        print ("\n*************\nlistings: {0}".format(listings))
        for listing in listings:
            title = listing.xpath('a[@class="result-title hdrlnk"]/text()').extract_first()
            price = listing.xpath('span[@class="result-meta"]/span[@class="result-price"]/text()').extract()
            neighbourhood = listing.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract()
            area_list = listing.xpath('span[@class="result-meta"]/span[@class="housing"]/text()').extract()

            # processing neighbourhood info
            if neighbourhood:
                neighbourhood = str(neighbourhood[0]).replace('(','').replace(')','').strip()
            else:
                neighbourhood = "UNKNOWN"

            # process space info
            if area_list[0]:
                # remove trailing '-'
                space = str(str(area_list[0]).strip().strip('\n').split('-')[-1]).strip()
                if not space:
                    space = "0ft"
            
            yield {'Title': title, 'Hood': neighbourhood, 'Price': price, 'Area': space}
