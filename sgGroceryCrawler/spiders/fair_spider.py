import scrapy

from sgGroceryCrawler.items import SggrocerycrawlerItem

class FairSpider(scrapy.Spider):
    name = "fair_spider"
    allowed_domains = ["www.fairprice.com.sg"]
    
    start_urls = [
        "http://www.fairprice.com.sg/webapp/wcs/stores/servlet/CategoryDisplay?storeId=10001&urlRequestType=Base&pageView=grid&catalogId=10051&categoryId=13501&beginIndex=0",
    ]

    def parse(self, response):

        # first step, parse the list of items 
        for sel in response.xpath('//div[@class="products grid_mode"]/div[@class="pr_nlst_wrp"]'):
            item = SggrocerycrawlerItem()

            item['title'] = sel.xpath('a[2]/h3/text()').extract()[0]
            item['small_img'] = sel.xpath('a[1]/p/img/@src').extract()[0]
            
            #This is small image url
            #we might be able to 'guess' the smaller and larger image url
            #look at the pattern below:
            #http://s3-ap-southeast-1.amazonaws.com/www.fairprice.com.sg/fpol/media/images/product/XL/10274312_XL1.jpg
            #http://s3-ap-southeast-1.amazonaws.com/www.fairprice.com.sg/fpol/media/images/product/L /10274312_L1.jpg
            #http://s3-ap-southeast-1.amazonaws.com/www.fairprice.com.sg/fpol/media/images/product/M /10274312_M1.jpg

            old_price = sel.xpath('div[@class="list_price"]/span/text()').extract()
            if len(old_price) is not 0:
                item['old_price'] = old_price[0]
            
            item['now_price'] = sel.xpath('span[@class="pl_lst_rt"]/text()').extract()[0]
            item['prd_url'] = sel.xpath('a[2]/@href').extract()[0]
            
            availability = sel.xpath('div[@class="pro_stock"]/span/text()').extract()[0]
            print 'availability is ' + availability
            
            
            item['merchant'] = "Fairprice"
            item['website'] = "http://www.fairprice.com.sg"

            yield item


        # second step, navigate to the next product list page
        # eg. www.fairprice.com.sg/.../categoryId=13501&beginIndex=0
        list1 = response.url.split('categoryId=')
        list2 = list1[1].split('&beginIndex=')
        catId = int(list2[0])
        beginInd = int(list2[1])

        # if there are items in current page, then go to next page
        # then go to next page by changing the beginIndex
        if (len(response.xpath('//fieldset/div/div'))):
            splitList = response.url.split('beginIndex=')
            new_url = splitList[0] + 'beginIndex=' + str(beginInd + 24)
            print '>>> next page url is ' + new_url
            yield scrapy.Request(new_url, callback=self.parse)
            
        # if current page has 0 items, but it's not first page
        # then go to next category by change categoryId and reset beginIndex
        elif (beginInd != 0):
            splitList = response.url.split('categoryId=')
            new_url = splitList[0] + 'categoryId=' + str(catId + 1) + '&beginIndex=0'
            print '>>> next category url is ' + new_url
            yield scrapy.Request(new_url, callback=self.parse)
            
        # if current page has 0 item, and is the first page of the category
        # stop the crawl, cuz we reach the end
        else:
            print '>>> We have finished the crawling. Thanks and good night. '
