import json,pymysql

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

def open_json():
	filepath = r'F:\Scrapy\IP_jiangxianli\freeip-json\-liangxianli.com_2019-02Month-.json'
	with open(filepath,'r') as f:
		lines = f.readlines()
		for line in lines:
			ip = json.loads(line)
			yield ip


def insert_mysql(db,cur):
	sql_insert = '''INSERT INTO liangxianli(nume,protocol,ip,port) VALUES (%s,%s,%s,%s)'''
	
	ips = open_json()
	
	nume =1
	for ip in ips:
		ip_values = (nume,ip['protocol'],ip['ip'],ip['port'])
		try:
			cur.execute(sql_insert,ip_values)
			print('{0}成功写入MYSQL'.format(ip_values))
			db.commit()
		except:
			print('{0}写入MYSQL失败'.format(ip_values))
			db.rollback()
		nume +=1

if __name__ == '__main__':
	db,cur = connect_db()
	insert_mysql(db,cur)
	close_db(db)