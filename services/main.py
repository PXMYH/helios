#!/usr/bin/env python

import logging
import json
from flask import Flask
from scrapy.crawler import CrawlerRunner
from craigslist.craigslist.spiders.craigbot import CraigbotSpider
# from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'main:crawl_for_listings',
            'trigger': 'interval',
            'seconds': 60
        }
    ]

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

    SCHEDULER_API_ENABLED = True


app = Flask('Scrapy With Flask')
# app.config.from_object(Config())

crawl_runner = CrawlerRunner()      # requires the Twisted reactor to run
rental_list = []                    # store links to be scraped
scrape_in_progress = False
scrape_complete = False


@app.route('/')
def welcome():
    return "Welcome to Helios System!", 200


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
    from apscheduler.schedulers.twisted import TwistedScheduler
    import os

    # start the logger
    globalLogBeginner.beginLoggingTo([textFileLogObserver(stdout)])

    # start the WSGI server
    root_resource = wsgi.WSGIResource(reactor, reactor.getThreadPool(), app)
    factory = server.Site(root_resource)
    http_server = endpoints.TCP4ServerEndpoint(reactor, 9999)
    http_server.listen(factory)

    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    scheduler = TwistedScheduler()
    scheduler.add_job(crawl_for_listings, 'interval', seconds=60)
    scheduler.start()
    print (
        'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # start event loop
    try:
        logging.debug("initiating helios system ...")
        reactor.run()
    except (KeyboardInterrupt, SystemExit):
        pass
