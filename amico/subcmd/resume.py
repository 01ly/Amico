
import threading, time
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):

    def parse(self,cmdname,args,spiders):
        argv = args[0]
        if argv == 'spiders':
            return '\r\n Not a valid usage of command: resume <spider name>'
        d = {i.name:i for i in spiders}
        if argv in d:
            spider = d[argv]
            if spider.status == 'RUNNING':
                return f"* Spider {argv} is running,it can not resume. "
            elif spider.status == 'PAUSE' or \
                 spider.status == 'STOP':
                lock = threading.Lock()
                lock.acquire()
                spider.status = 'RESUME'
                spider._resume_at = time.ctime()
                lock.release()
                return f'[resume],{argv}'
            elif spider.status == 'RESUME':
                return f'* Spider {argv} is resuming.'
            else:
                return f'* Invalid resuming status "{spider.status}" for a spider.'
        else:
            return f'* No spider "{argv}" in the project.'
