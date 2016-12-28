# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mls.items import MlsItem
import codecs

class RealtorSpider(CrawlSpider):
    name = "realtor"
#    allowed_domains = ["www.reddit.com"]
#    start_urls = ['https://www.reddit.com/r/pics/']
    
    allowed_domains = ["estateblock.com"]
    start_urls = ['https://www.estateblock.com/lower-mainland/homes/0-700000_price/49.274356888946244,-123.16317558288574,49.29384075153085,-123.10824394226074_bound/14_zm']
    
    rules = [
    	Rule(LinkExtractor(allow=['/vancouver-real-estate/\w*']),
                        callback='parse_item',
                        follow=True)
    ]

    def parse_item(self, response):
        with codecs.open("response.html", "w") as f:
            f.write(response.body)
#        print ("_______ response is " + str(response.body) )
        selector_list = response.css('div.thumbnail')
        selector_list_extract = response.xpath('//div[@class="thumbnail"]').extract()
        with codecs.open("selectorlist.html", "w") as w:
            w.write(str(selector_list_extract))

        for idx, selector in enumerate(selector_list):
            mls_item = MlsItem()
            print "^^^^^^^ idx = " + str(idx) + " selector = " + selector.extract() + " count = " + str(len(selector_list))
            
            mls_item['address'] = selector.css('address.truncate::text').extract()
            mls_item['mls_num'] = selector.css('div.col-md-6.sm-text-left.md-text-right').xpath('small[contains(., "MLS")]/span/text()').extract()
            mls_item['maint_fee'] = selector.css('div.col-md-6').xpath('small[contains(., "Maint")]/span/text()').extract()
            mls_item['price'] = selector.css('div.price span::text').extract()
            # need to post processing price list (price, structure, sqft)
            mls_item['built_year'] = selector.css('div.col-md-6.sm-text-left.md-text-right').xpath('small[contains(., "built")]/span/text()').extract()
            
#            mls_item['house_type'] = selector.xpath('//div[@class="col-md-7"]/small/text()').extract()
#            mls_item['price'] = selector.xpath('//div[@class="price"]/span/text()').extract()
#            mls_item['price'] = response.xpath('div.price').xpath('//div/label/meta[contains(@itemprop, "price")]').re(r'.*price".*')
#            mls_item['link_url'] = response.xpath('//div/address/a/@href').extract()
#            mls_item['link_url'] = response.css('li.col-lg-6').xpath('//div/address/a/@href').extract()

            yield mls_item
