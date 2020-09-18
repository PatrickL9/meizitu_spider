import re
import requests
from scrapy import Request
from scrapy.spiders import Spider
from ..items import MeizituSpiderItem

class meizitu_spider(Spider):
    name = 'meizitu_crawl'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',

    }
    first_url = 'https://www.mzitu.com/'

    def start_requests(self):
        yield Request(self.first_url, headers=self.headers)

    def parse(self, response, **kwargs):
        # 爬取每个套图的入口链接
        meizi_urls = response.xpath('//div[@class="postlist"]/ul[@id="pins"]/li/span/a[@target="_blank"]/@href').extract()
        # 获取套图标题，并作为meta传参下去，后面用于文件夹起名
        file_names = response.xpath('//div[@class="postlist"]/ul[@id="pins"]/li/span/a[@target="_blank"]/text()').extract()
        for meizi_url, file_name in zip(meizi_urls, file_names):
            yield Request(meizi_url, headers=self.headers, meta={'file_name' : file_name, 'referer' : meizi_url}, callback=self.parse_meizi)

        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()
        next_url1 = ''.join(next_url)
        yield Request(next_url1, headers=self.headers)

    def parse_meizi(self, response):
        item = MeizituSpiderItem()
        file_name = response.meta['file_name']
        img_url_temp = response.xpath('//div[@class="main-image"]/p/a/img/@src').extract()
        img_url = ''.join(img_url_temp)
        item['img_name'] = re.findall('.+/(.+)$',img_url)
        item['img_url'] = img_url_temp
        item['file_name'] = file_name
        item['referer'] = response.meta['referer']
        yield item
        next_page = response.xpath('//div[@class="pagenavi"]/a[last()]/span/text()').extract()
        # print(next_page)
        # print(re.search('下一页',str(next_page)))
        if re.search('下一页',str(next_page)):
            next_url = response.xpath('//div[@class="pagenavi"]/a[last()]/@href').extract()
            next_url1 = ''.join(next_url)
            # print('在运行下一页辣')
            # print(next_url1)
            yield Request(next_url1, headers=self.headers, meta={'file_name' : file_name, 'referer' : next_url1}, callback=self.parse_meizi)


