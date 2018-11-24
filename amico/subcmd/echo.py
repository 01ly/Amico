
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):

    def parse(self,cmdname,args,spiders):
        argv = args[0]
        if argv == 'spiders':
            return '\r\n Not a valid usage of command: echo <spider name>'
        prompt = ''
        d = {i.name:i for i in spiders}
        if argv in d:
            spider = d[argv]
            sp = f'''----------------Spider-{argv}-------------------
            \r\n- Name:{spider.name}  Status:{spider.status}
            \r\n- Class:{spider.__class__.__name__}
            \r\n- Priority:{spider.priority} 
            \r\n- SeedUrls:{spider.urls}
            \r\n- Path:{spider.settings.PATH}
            \r\n- Session:{spider.session}
            \r\n- StartAt:{spider._start_at}
            \r\n{'-'*50}
            '''
            prompt += sp
        else:
            return f'* No spider "{argv}" in the project.'
        return prompt
