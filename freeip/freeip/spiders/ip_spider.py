import scrapy
import time,json
from freeip.items import FreeipItem

class FIpSpider(scrapy.Spider):
    name = 'freeip'
    allowed_domains = ['jiangxianli.com']

    jxl_api = 'http://ip.jiangxianli.com/api/proxy_ips?page='
    pages = 7

    def start_requests(self):
        for pg in range(1,self.pages):
            url = '{0}{1}'.format(self.jxl_api,pg)
            yield scrapy.Request(url,callback=self.parse_ip)

    def parse_ip(self,response):
        plain_txt = response.text
        dict_ips = json.loads(plain_txt)
        iproxy = dict_ips['data']['data']

        print('链接:{0},页数:{1}'.format(response.url, dict_ips['data']['current_page']))
        print('获取到的IP数量:{}'.format(len(iproxy)))

        for ip in iproxy:
            IPitem = FreeipItem()
            IPitem['ip'] = ip['ip']
            IPitem['port'] = ip['port']
            IPitem['protocol'] = ip['protocol']

            yield IPitem
