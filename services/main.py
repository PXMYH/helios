#!/usr/bin/env python

import logging
import json
from flask import Flask
from scrapy.crawler import CrawlerRunner
from craigslist.craigslist.spiders.craigbot import CraigbotSpider

app = Flask('Scrape With Flask')
crawl_runner = CrawlerRunner()      # requires the Twisted reactor to run
rental_list = []                    # store links to be scraped
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
        global rental_list
        # start the crawler and execute a callback when complete
        eventual = crawl_runner.crawl(CraigbotSpider, rental_list=rental_list)
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
        return json.dumps(rental_list)
    return 'Scrape Still Progress'


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True


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
    logging.debug("initiating helios system ...")
    reactor.run()
