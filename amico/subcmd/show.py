
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):

    def parse(self,cmdname,args,spiders):
        argv = args[0]
        if argv != 'spiders':
            return '\r\n Not a valid usage of command: show spiders'
        prompt = ''
        for _,spider in enumerate(spiders):
            sp = f'''----------------Spider-{_}-------------------
            \r\n- Name:{spider.name}  Status:{spider.status}
            \r\n- Class:{spider.__class__.__name__}
            \r\n- Priority:{spider.priority} 
            \r\n- SeedUrls:{spider.urls}
            \r\n- Path:{spider.settings.PATH}
            \r\n- Session:{spider.session}
            \r\n- StartAt:{spider._start_at}
            '''
            prompt += sp
        return prompt
