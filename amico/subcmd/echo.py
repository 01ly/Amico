
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
            cd = f'''
            \r\n- UrlFilter:count[{spider.urlfilter.count}] capacity[{spider.urlfilter.capacity}] error_rate[{spider.urlfilter.error_rate}]
            \r\n- HtmlFilter:count[{spider.respfilter.count}] capacity[{spider.respfilter.capacity}] error_rate[{spider.respfilter.error_rate}]
            ''' if spider.urlfilter and spider.respfilter else ''
            sp = f'''
            \r\n----------------Spider-{argv}-------------------
            \r\n- Name:{spider.name}  Status:{spider.status}
            \r\n- Class:{spider.__class__.__name__}
            \r\n- Success:{spider._success}    Fail:{spider._fail}     Exception:{spider._exc}'''+ cd +f'''
            \r\n- Priority:{spider.priority} 
            \r\n- SeedUrls:{spider.urls}
            \r\n- Path:{spider.settings.PATH}
            \r\n- Session:{spider.session}
            \r\n- StartAt:{spider._start_at}
            \r\n- PausedAt:{spider._pause_at}
            \r\n- ResumeAt:{spider._resume_at}
            \r\n- StopAt:{spider._stop_at}
            \r\n- RestartAt:{spider._restart_at}
            \r\n- CloseAt:{spider._close_at}
            \r\n{'-'*50}
            '''
            prompt += sp
        else:
            return f'* No spider "{argv}" in the project.'
        return prompt
