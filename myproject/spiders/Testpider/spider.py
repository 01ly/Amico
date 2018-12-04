import amico
from amico import send,Request,Url
from bs4 import BeautifulSoup as bs

class TestpiderSpider(amico.Spider):

    # The unique name of the spider.It's necessary.
    # Its priority is higher than the NAME in settings.py
    # of the spider.If you override it,the spider name will
    # be the overrides one.
    name = 'testpider'
    #the start urls of the spider
    urls = ['https://segmentfault.com/']

    def parse(self,response):
        #do something with the response.
        #url = some url parsed from the response
        # print(f'{response.url}: {self._success} {self._fail} {self._exc} '
        # 	  f'-->{response.spider.urlfilter.count} {len(response.spider.urlfilter)} {response.spider.respfilter.count}<--')
        text = response.read()
        html = bs(text, 'lxml')
        links = html('a')
        a = 0
        for i in links:
            if hasattr(i, 'href'):
                if a >= 3:
                    break
                try:
                    send(Request(self, i['href']))
                    a += 1
                except:
                    continue
        # or return a Request
        # return Request(self,url,...)

