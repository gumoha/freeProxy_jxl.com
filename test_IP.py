import requests,json,random

def ip_yield():
	filepath = r'F:\Scrapy\IP_jiangxianli\freeip-json\-liangxianli.com_2019-02Month-.json'
	with open(filepath,'r') as f:
		ips = f.readlines()
		for line in ips:
			ip = json.loads(line)
			yield (ip)

def ip_list():
	filepath = r'F:\Scrapy\IP_jiangxianli\freeip-json\-liangxianli.com_2019-02-21-.json'
	with open(filepath,'r') as f:
		ips = [ json.loads(line) for line in f.readlines()]
	
	return ips
			
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

	checkurl = [
					'https://cn.bing.com/',\
					'https://www.qdaily.com/',\
					'https://www.bilibili.com/',\
					'https://weibo.com/',\
					'https://cd.lianjia.com/',\
					'https://www.taobao.com/',\
					'https://www.amazon.cn/',
				]
				
	checkNum = 0
	
	new_ip = {'{0}'.format(ip['protocol']):'{0}:{1}'.format(ip['ip'],ip['port'])}
	
	for url in checkurl:
		try:
			req = requests.get(url=url,proxies = new_ip,headers=random.choice(hds),timeout=5)
			if req.status_code ==200:
				#print('测试网址:{0},测试IP{1}——成功~~~'.format(url,ip))
				checkNum +=1
		except:
			print('测试网址:{0},测试IP{1}——失败！！！'.format(url,new_ip))
			
	if checkNum >=6:
		return True
	else:
		return False


if __name__ =='__main__':
	invalid_ip =[]
	for ip in ip_yield():
		if ipCheck(ip) is True:
			print('此ip：{} 验证可用~~~'.format(ip))
		else:
			print('此ip：{} 验证不可用!!!'.format(ip))
			invalid_ip.append(ip)
	
	print('无效的IP:\n {}'.format(invalid_ip))
	