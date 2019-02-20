import scrapy
import time,json,random
from freeip.items import FreeipItem

class FIpSpider(scrapy.Spider):
    name = 'freeip'
    allowed_domains = ['jiangxianli.com']

    jxl_api = 'http://ip.jiangxianli.com/api/proxy_ips?page='
    pages = 10

    def start_requests(self):
        for pg in range(1,self.pages):
            url = '{0}{1}'.format(self.jxl_api,pg)
            time.sleep(random.choice(range(3)))
            yield scrapy.Request(url,callback=self.parse_ip)

    def parse_ip(self,response):
        plain_txt = response.text
        dict_ips = json.loads(plain_txt)
        iproxy = dict_ips['data']['data']

        print('请求header {}'.format(response.request.headers))
        print('链接:{0},页数:{1}'.format(response.url, dict_ips['data']['current_page']))
        print('获取到的IP数量:{}'.format(len(iproxy)))

        for ip in iproxy:
            ip = {'{0}'.format(ip['protocol']): '{0}:{1}'.format(ip['ip'], ip['port'])}
            if self.ipCheck(ip) is True:
                print('此ip {0} 验证可用，保存~~~'.format(ip))
                IPitem = FreeipItem()
                IPitem['ip'] = ip['ip']
                IPitem['port'] = ip['port']
                IPitem['protocol'] = ip['protocol']

                yield IPitem

            else:
                print('此ip {0} 验证不可用，丢弃！！！'.format(ip))

    def ipCheck(self,ip):
        checkurl = 'https://cd.lianjia.com/ershoufang/'
        try:
            req = scrapy.Request(url=checkurl, proxies=ip, timeout=5)
            print(req.status_code)
            if req.status_code == 200:
                return True
        except:
            return False
