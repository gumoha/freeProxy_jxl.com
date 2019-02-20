import requests,json,random,time

def ip_spider():
	url2 = 'http://ip.jiangxianli.com/api/proxy_ips?page='
	pages = 10

	for pg in range(1,pages):
		url = '{0}{1}'.format(url2,pg)
		
		time.sleep(random.choice(range(3)))
		
		req=requests.get(url)
		plain_txt = req.content

		dict_ips=json.loads(plain_txt)

		print('链接:{0},页数:{1}'.format(url,dict_ips['data']['current_page']))

		iproxy = dict_ips['data']['data']
		print('获取到的IP数量:{}'.format(len(iproxy)))

		for ip in iproxy:
			#ip = '{0}://{1}:{2}'.format(ip['protocol'],ip['ip'],ip['port'])
			ip = {'{0}'.format(ip['protocol']):'{0}:{1}'.format(ip['ip'],ip['port'])}
			yield ip
			
def ipCheck(ip):
	#Some User Agents
	hds=[
		{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
		{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
		{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
		{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'},\
		{'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
		{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
		{'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
		{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
		{'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
		{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
		{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
		{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
		{'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
		{'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}
		]

	checkurl = 'https://cd.lianjia.com/ershoufang/'
	try:
		req = requests.get(url=checkurl,proxies = ip,headers=random.choice(hds),timeout=5)
		if req.status_code == 200:
			return True
	except:
		return False


if __name__ =='__main__':
	ips = ip_spider()
	with open("F:\Scrapy\IP_jiangxianli\-FreeIP_liangxianliIP-.json",'w') as f:
		for ip in ips:
			if ipCheck(ip) is True:
				print('此ip：%s 验证可用，保存~~~' % ip)
				line = json.dumps(dict(ip), ensure_ascii=False) + '\n'
				f.write(line)
			else:
				print('此ip：%s 验证不可用，丢弃！' % ip)