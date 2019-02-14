import amico
from amico import send,Request

class ${SpiderName}Spider(amico.Spider):

    # The unique name of the spider.It's necessary.
    # Its priority is higher than the NAME in settings.py
    # of the spider.If you override it,the spider name will
    # be the overrides one.
    name = '${spider_name}'
    #the start urls of the spider
    urls = []

    def parse(self,response):
        #do something with the response.
        #url = some url parsed from the response
        ...
        send(Request(self,url,...))
        # or return a Request
        # return Request(self,url,...)

