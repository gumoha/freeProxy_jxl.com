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
        self.file = codecs.open(filen,'a')

    def close_spider(self,spider):
        self.file.close()

    def process_item(self, item, spider):
        print('验证搜集到的IP……')
        ip = '{0}://{1}:{2}'.format(item['protocol'],item['ip'],item['port'])
        if self.ipCheck(ip) is True:
            print('此ip：%s 验证可用，保存！' % ip)
            line = json.dumps(dict(ip), ensure_ascii=False) + '\n'
            self.file.write(line)
        else:
            print('此ip：%s 验证不可用，丢弃！' % ip)
            raise DropItem(item)

        return item

    def ipCheck(self,ip):
        checkurl = 'https://cd.lianjia.com/ershoufang/'

        try:
            req = requests.get(checkurl,proxies = ip,timeout=3)
            if req.status_code == 200:
                return True
        except:
            return False
