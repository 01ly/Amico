
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):


    def parse(self,cmdnae,args,spiders):
        prompt = ''
        for _,i in enumerate(spiders):
            p = f'''
            \r\n*{'-'*60}*
            \r\n{_+1}. {i.name} | {i.status} | {i.__class__.__name__} | Success:{i._success}  Fail:{i._fail}  Exception:{i._exc}
            '''
            prompt += p
        return prompt


