
#coding:utf-8

import amico
from amico import Url,Request

class TTspider(amico.Spider):
	urls = ['https://blog.csdn.net',]
	name = 'linkin'
	# blacklist = [
	# 	Url(domain='segmentfault.com'),
	# ]
	rules = [
		# Url(domain='blog.csdn.net',callback='test')
	]

	def test(self,response):
		print(222222222)

	def tt(self,response):
		print(1111111)

	def parse(self,response):
		print(self)
		print(response.read()[:100])
		# print(response.json())
		for i in range(10):
			self.send(Request(self,'https://blog.csdn.net/xiecj_2006/article/details/42464681'))
		# self.send(response.url)
