import sys
import json
import os


from crawler.crawl import crawl
from datetime import datetime

spider_name = os.getenv('SPIDER_NAME')

def scrape(event={}, context={}):
    crawl(spider_name=spider_name)

if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)
