import scrapy
import time,random
from freeip.items import FreeipItem

class FIpSpider(scrapy.Spider):
    name = 'freeip'
    allowed_domains = ['jiangxianli.com']

    jxl_api = 'http://ip.jiangxianli.com/api/proxy_ips'

    def start_requests(self):
        yield scrapy.Request(self.jxl_api,callback=self.parse_ip)

    def parse_ip(self,response):
        pass