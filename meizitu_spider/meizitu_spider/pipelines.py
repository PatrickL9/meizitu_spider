# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from meizitu_spider.settings import IMAGES_STORE

class MeizituSpiderPipeline(ImagesPipeline):
    browser = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    def get_media_requests(self, item, info):
        img_url = ''.join(item['img_url'])
        # print('pipe:' + img_url)
        yield Request(img_url, headers={'User-Agent' : self.browser, 'referer' : item['referer']}, meta={'file_name':item['file_name'], 'img_name': item['img_name']})

    def file_path(self, request, response=None, info=None):
        title = request.meta['file_name']
        img_name = ''.join(request.meta['img_name'])
        image_store = os.path.join(IMAGES_STORE,title)
        if not os.path.exists(image_store):
            os.makedirs(image_store)
        file_name = os.path.join(image_store, img_name)
        # print('pipe:' + file_name)
        return file_name
