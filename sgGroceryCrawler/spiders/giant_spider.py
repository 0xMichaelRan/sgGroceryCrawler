import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sgGroceryCrawler.items import SggrocerycrawlerItem


class GiantSpider(CrawlSpider):
    name = "giant_spider"
    allowed_domains = ["giantonline.com.sg"]
    
    start_urls = ['https://giantonline.com.sg/']
    # urls from which the spider will start crawling
    
    rules = [
        Rule(LinkExtractor(allow=[r'catalog/.+']), follow=True, 
            callback='parse_item'),
    ]

    def parse_item(self, response):

        for sel in response.xpath('//div[@class="items"]/div'):
            item = SggrocerycrawlerItem()

            item['brand'] = sel.xpath('div/div/a/text()').extract()
            item['title'] = sel.xpath('div/div/h3/a/text()').extract()

            item['small_img'] = sel.xpath('div/a/div/img/@src').extract()

            item['old_price'] = sel.xpath('div/div/div/div/div/text()').extract()
            item['now_price'] = sel.xpath('div/div/div/div/div/strong/text()').extract()

            item['prd_code'] = sel.xpath('div/div/div/div/text()[1]').extract()

            item['merchant'] = "Giant"
            item['website'] = "http://giantonline.com.sg"

            yield item
