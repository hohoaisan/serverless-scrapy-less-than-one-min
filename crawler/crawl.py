# my_sls_scraper/crawl.py
import sys
import imp
import os
import logging
from urllib.parse import urlparse

from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import scrapydo

# Need to "mock" sqlite for the process to not crash in AWS Lambda / Amazon Linux
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")

scrapydoEnabled = True
feedFormat = 'csv'

def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None


def crawl(settings={}, spider_name="", spider_kwargs={}):
    project_settings = get_project_settings()

    print(project_settings.copy_to_dict())
    spider_loader = SpiderLoader(project_settings)

    spider_cls = spider_loader.load(spider_name)

    feed_uri = ""

    if is_in_aws():
        # Lambda can only write to the /tmp folder.
        settings['HTTPCACHE_DIR'] = "/tmp"
        feed_uri = f"s3://{os.getenv('FEED_BUCKET_NAME')}/{spider_name}/{spider_name}-%(time)s.{feedFormat}"
    else:
        feed_uri = f'file://{os.getcwd()}/{spider_name}-%(time)s.{feedFormat}'

    settings['FEEDS'] = {
        feed_uri: {
            'format': feedFormat,
            'encoding': 'utf8',
        }
    }

    if scrapydoEnabled:
        scrapydo.setup()
        scrapydo.default_settings.update({**project_settings, **settings})
        scrapydo.run_spider(spider_cls, **spider_kwargs)
    else:
        # Will throw ReactorNotRestartable on AWS lambda
        process = CrawlerProcess({**project_settings, **settings})
        process.crawl(spider_cls, **spider_kwargs)
        process.start()
