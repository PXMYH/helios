#!/usr/bin/env python

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from testspiders.spiders.followall import FollowAllSpider
from scrapy.xlib.pydispatch import dispatcher
from craigslist import CraigbotSpider

def stop_reactor():
    reactor.stop()

def main():
    print ("Eagle Eye System Initiated ...")
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    spider = FollowAllSpider(CraigbotSpider)
    crawler = Crawler(Settings())
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    log.msg('Running reactor...')
    reactor.run()  # the script will block here until the spider is closed
    log.msg('Reactor stopped.')


if __name__ == "__main__":
    main()
    