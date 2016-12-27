# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MlsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
#    image_urls = Field()
#    images = Field()
    address = Field()
    price = Field()
    maint_fee = Field()
    built_year = Field()
    house_type = Field()
    link_url = Field()
    mls_num = Field()
