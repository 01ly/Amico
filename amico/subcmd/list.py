
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):


    def parse(self,cmdnae,args,spiders):
        prompt = ''
        for i in spiders:
            p = f'''{'-'*60}
            \r\n - {i.name} | {i.status} | {i.__class__.__name__} | {i._start_at}
            \r\n{'-'*60}
            '''
            prompt += p
        return prompt


