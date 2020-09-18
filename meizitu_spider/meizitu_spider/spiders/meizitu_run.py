from scrapy import cmdline

name = 'meizitu_crawl'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())