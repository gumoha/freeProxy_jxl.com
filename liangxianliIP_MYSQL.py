import requests,random,time
import json,pymysql

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
	
	for url in checkurl:
		try:
			req = requests.get(url=url,proxies = ip,headers=random.choice(hds),timeout=5)
			if req.status_code ==200:
				#print('测试网址:{0},测试IP{1}——成功~~~'.format(url,ip))
				checkNum +=1
		except:
			print('测试网址:{0},测试IP{1}——失败！！！'.format(url,ip))
			pass
			
	if checkNum >=4:
		return True
	else:
		return False
		
def connect_db():
	try:
		db = pymysql.connect(host='127.0.0.1',
								port=3306,
								user='banquan',
								password='12345',
								db='freeproxy')
		
		cur = db.cursor()
		print('数据库连接成功！')
		return db,cur
	except:
		print('连接数据库失败！')
		return None
		
def close_db(db):
	
	db.close()
	print('关闭数据库')	
		
def insert_mysql(db,cur):
	sql_insert = '''INSERT INTO liangxianli(protocol,ip,port) VALUES (%s,%s,%s)'''
	
	ips = ip_spider()
	for ip in ips:
		if ipCheck(ip) is True:
			print('此ip：%s 验证可用，保存MYSQL~~~' % ip)
			ip_values = (ip['protocol'],ip['ip'],ip['port'])
			try:
				cur.execute(sql_insert,ip_values)
				print('成功写入MYSQL')
				db.commit()
			except:
				print('写入MYSQL失败')
				db.rollback()
		else:
			print('此ip：%s 验证不可用，丢弃！' % ip)
			
if __name__ == '__main__':
	db,cur = connect_db()
	insert_mysql(db,cur)
	close_db(db)