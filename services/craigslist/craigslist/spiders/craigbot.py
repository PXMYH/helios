# -*- coding: utf-8 -*-
import datetime
# from postgres.postgres import Rental
from services.postgres.postgres import Rental
from os import path
from scrapy import Request
import scrapy
import sys
# sys.path.insert(0, "/Users/ProjectX/workspace/helios/services")


class CraigbotSpider(scrapy.Spider):
    name = 'craigbot'
    allowed_domains = ['craigslist.org']
    # TODO: accept search URL from command line
    # tweak start_urls to get to the result faster
    # start_urls = ['https://vancouver.craigslist.org/search/apa']
    start_urls = [
        'https://vancouver.craigslist.org/search/van/apa?min_bedrooms=2&max_bedrooms=2']

    def parse(self, response):
        print ("[HELIOS] Response: {0}\n".format(response.body))
        listings = response.xpath('//p[@class="result-info"]')
        print ("[HELIOS] Listings: {0}".format(listings))
        for listing in listings:
            # get relative url and construct absolute url
            # relative_url = listing.xpath('a/@href').extract_first()
            # print ("relative url {0}".format(relative_url))
            # absolute_url = response.urljoin(relative_url)

            title = listing.xpath(
                'a[@class="result-title hdrlnk"]/text()').extract_first()
            price = listing.xpath(
                'span[@class="result-meta"]/span[@class="result-price"]/text()').extract()
            neighbourhood = listing.xpath(
                'span[@class="result-meta"]/span[@class="result-hood"]/text()').extract()
            area_list = listing.xpath(
                'span[@class="result-meta"]/span[@class="housing"]/text()').extract()

            # processing neighbourhood info
            if neighbourhood:
                neighbourhood = u''.join((neighbourhood[0])).encode('utf-8').replace(
                    '(', '').replace(')', '').strip()
            else:
                neighbourhood = "UNKNOWN"

            # process space info
            if area_list[0]:
                # remove trailing '-'
                space = str(str(area_list[0]).strip().strip(
                    '\n').split('-')[-1]).strip()
                if not space:
                    space = "0ft"

            space_num = space.strip('ft')
            if int(space_num) != 0 and space and price:
                unit_price = round(
                    int(str(price[0]).strip('$')) / int(space_num), 1)
            else:
                unit_price = -1

            yield {'Title': title, 'Hood': neighbourhood, 'Price': price, 'Area': space, 'UnitPrice': unit_price}

            updated_at = datetime.datetime.utcnow()

            if not price:
                print (
                    "price is somehow empty, this most likely is an error on Craigslist posting")
                self.save_to_db(neighbourhood, "2", "2", "0", "0", updated_at)
                self.rental_list.append({
                    'location': neighbourhood,
                    'bedroom': '2',
                    'bathroom': '2',
                    'den': '0',
                    'price': 'nil'
                })
            else:
                self.save_to_db(neighbourhood, "2", "2",
                                "0", str(price[0]).strip('$').encode('ascii', 'ignore'), updated_at)
                self.rental_list.append({
                    'location': neighbourhood,
                    'bedroom': '2',
                    'bathroom': '2',
                    'den': '0',
                    'price': str(price[0]).strip('$').encode('ascii', 'ignore')
                })

        relative_next_url = response.xpath(
            '//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)
        print ("[HELIOS] Relative Next URL: {0}".format(relative_next_url))
        print ("[HELIOS] Absolute Next URL: {0}".format(absolute_next_url))

        yield Request(absolute_next_url, callback=self.parse)

    def save_to_db(self, location, bedroom, bathroom, den, price, updated_at):
        rental_instance = Rental(
            location, bedroom, bathroom, den, price, updated_at)
        rental_instance.save_record()
