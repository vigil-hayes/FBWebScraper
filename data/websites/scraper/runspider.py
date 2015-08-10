from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from spiders.dmoz_spider import DmozSpider

def runspider():
	spider = DmozSpider()
	crawler = Crawler(Settings())
	#crawler.configure()
	crawler.crawl(spider)
	#crawler.start()
	#log.start()
	#reactor.run() # the script will block here
