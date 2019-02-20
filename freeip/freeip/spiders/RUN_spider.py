from scrapy import cmdline

name = 'freeip'

cmd = 'scrapy crawl %s'%name

cmdline.execute(cmd.split())