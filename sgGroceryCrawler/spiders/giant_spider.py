import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from sgGroceryCrawler.items import SggrocerycrawlerItem


class GiantSpider(CrawlSpider):
    name = "giant_spider"
    allowed_domains = ["giantonline.com.sg"]
    
    start_urls = ['https://giantonline.com.sg/catalog/dairy-frozen/chilled-juice']
    # urls from which the spider will start crawling
    
    rules = [
        Rule(LinkExtractor(allow=[r'catalog/[^/\?]+/[^/\?]+$',
                                  r'catalog/[^/\?]+/[^/\?]+\?Product_page=\d+$'
                            ]), follow=True, 
                            callback='parse_item'),
        
        # allow 2 kinds of links, eg:
        # https://giantonline.com.sg/catalog/dairy-frozen/chilled-juice/
        # https://giantonline.com.sg/catalog/dairy-frozen/chilled-juice?Product_page=2
    ]

    def parse_item(self, response):

        for sel in response.xpath('//div[@class="items"]/div/div'):
            item = SggrocerycrawlerItem()

            item['brand'] = sel.xpath('div[2]/a/text()').extract()[0]
            item['title'] = sel.xpath('div/h3/a/text()').extract()[0]

            item['small_img'] = ('https://giantonline.com.sg' + 
                                 sel.xpath('a/div/img/@src').extract()[0])

            # old_price may not exist
            old_price = sel.xpath('div/div/div/div/text()').extract()
            if len(old_price) is not 0:
                item['old_price'] = old_price[0]

            item['now_price'] = sel.xpath('div/div/div/div/strong/text()').extract()[0]

            item['prd_code'] = sel.xpath('div/div/div/text()[1]').extract()[0]

            item['merchant'] = "Giant"
            item['website'] = "http://giantonline.com.sg"

            yield item
