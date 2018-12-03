
#coding:utf-8

import amico
from amico import Url,Request,send
from bs4 import BeautifulSoup as bs

class TTspider(amico.Spider):

	name = 'linkin'
	urls = ['https://www.csdn.net/',]
	whitelist = [
		Url(re='http.*.csdn.net.*'),
	]
	# rules = [
	# 	Url(domain='blog.csdn.net',filter=True)
	# ]

	def test(self,response):
		print(222222222)

	def tt(self,response):
		return  'ppppp'

	def parse(self,response):
		# print(self)
		# print(f'{response.url}: {self._success} {self._fail} {self._exc} '
		# 	  f'-->{response.spider.urlfilter.count} {len(response.spider.urlfilter)} {response.spider.respfilter.count}<--')
		text = response.read()
		html = bs(text,'lxml')
		links = html('a')
		a = 0
		for i in links:
			if hasattr(i,'href'):
				if a>=3:
					break
				try:
					send(Request(self, i['href']))
					a+=1
				except:
					continue

	def error(self,response):
		# print(response.url,response.status)
		print('错误的返回码:',response.status)


	# def fingerprint(self,response):
	# 	return 'ppppp'

	def ttt(self,res):
		return
