import sys, os
import csv
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  
import scrapy
import logging
from items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
#    allowed_domains = ["dmoz.org"]
    url=""
    start_urls = []
    # Read in the URL from the file
    with open("/Users/spiderwoman/Dropbox/CitizenNet/facebook/facebook-sdk/incomplete_07312015/tutorial/url.tmp", 'rb') as infile:
	try:
		csvreader = csv.reader(infile, delimiter="\t")
		for row in csvreader:
			url=row[0]
    		        start_urls.append(url)
	except Exception as e:
		logging.log(logging.ERROR, e)
	logging.log(logging.DEBUG, start_urls)
#    start_urls = ["http://www.ksut.org/"]
    def parse(self, response):
        for sel in response.xpath('//p/text()'):
            item = DmozItem()
            item['desc'] = sel.extract()
            yield item 
