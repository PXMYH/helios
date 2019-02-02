#!/usr/bin/env python

# from twisted.internet import reactor
# from scrapy.crawler import Crawler
# from scrapy.settings import Settings
# from scrapy import signals
# from testspiders.spiders.followall import FollowAllSpider
# from scrapy.xlib.pydispatch import dispatcher
# from craigslist import CraigbotSpider

import logging
import json
from flask import Flask
from scrapy.crawler import CrawlerRunner
from craigslist.craigslist.spiders.craigbot import CraigbotSpider

app = Flask('Scrape With Flask')
crawl_runner = CrawlerRunner()      # requires the Twisted reactor to run
link_list = []                    # store links to be scraped
scrape_in_progress = False
scrape_complete = False


@app.route('/crawl')
def crawl_for_listings():
    """
    Scrape for real estate listings
    """
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        global link_list
        # start the crawler and execute a callback when complete
        eventual = crawl_runner.crawl(CraigbotSpider, link_list=link_list)
        eventual.addCallback(finished_scrape)
        return 'SCRAPING'
    elif scrape_complete:
        return 'SCRAPE COMPLETE'
    return 'SCRAPE IN PROGRESS'


@app.route('/results')
def get_results():
    """
    Get the results only if a spider has results
    """
    global scrape_complete
    if scrape_complete:
        return json.dumps(link_list)
    return 'Scrape Still Progress'


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True
# def stop_reactor():
#     reactor.stop()
# def main():
#     print ("Eagle Eye System Initiated ...")
#     dispatcher.connect(stop_reactor, signal=signals.spider_closed)
#     spider = FollowAllSpider(CraigbotSpider)
#     crawler = Crawler(Settings())
#     crawler.configure()
#     crawler.crawl(spider)
#     crawler.start()
#     logging.info('Running reactor...')
#     reactor.run()  # the script will block here until the spider is closed
#     logging.info('Reactor stopped.')


if __name__ == '__main__':
    from sys import stdout
    from twisted.logger import globalLogBeginner, textFileLogObserver
    from twisted.web import server, wsgi
    from twisted.internet import endpoints, reactor

    # start the logger
    globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    # start the WSGI server
    root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    factory = server.Site(root_resource)
    http_server = endpoints.TCP4ServerEndpoint(reactor, 9999)
    http_server.listen(factory)

    # start event loop
    reactor.run()
