
import threading, time
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):

    def parse(self,cmdname,args,spiders):
        argv = args[0]
        if argv == 'spiders':
            return '\r\n Not a valid usage of command: restart <spider name>'
        d = {i.name:i for i in spiders}
        if argv in d:
            spider = d[argv]
            if spider.status == 'RUNNING':
                return f"* Spider {argv} is running,it can not restart. "
            elif spider.status == 'STOP':
                lock = threading.Lock()
                lock.acquire()
                spider.status = 'RESTART'
                spider._restart_at = time.ctime()
                lock.release()
                return f'* Spider {argv} restarted at {spider._restart_at} successfully.'
            elif spider.status == 'CLOSE':
                return f'* Spider {argv} is closed.'
            elif spider.status == 'PAUSE':
                return f'* Spider {argv} is paused.Using "resume" command to resume it.'
            else:
                return f'* Invalid resuming status "{spider.status}" for a spider.'
        else:
            return f'* No spider "{argv}" in the project.'
