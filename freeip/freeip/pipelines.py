# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs,json,requests
from scrapy.exceptions import DropItem


class FreeipPipeline(object):
    def open_spider(self,spider):
        filen = "F:\Scrapy\IP_jiangxianli\-FreeIP-.json"
        self.file = codecs.open(filen,'w')

    def close_spider(self,spider):
        self.file.close()

    def process_item(self, item, spider):
        #ip = '{0}://{1}:{2}'.format(item['protocol'],item['ip'],item['port'])
        ip = {'{0}'.format(item['protocol']): '{0}:{1}'.format(item['ip'], item['port'])}

        line = json.dumps(dict(ip), ensure_ascii=False) + '\n'
        self.file.write(line)

        return item
