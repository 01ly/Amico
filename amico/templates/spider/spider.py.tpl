import amico

class ${SpiderName}Class(amico.Spider):
    name = '${spider_name}'
    #the start urls of the spider
    urls = []
    #the priority of the current spider in the project,not necessary
    priority = 0

    def parse(self,response):
        #do something with the response.
        ...
        return amico.Request(self,)
