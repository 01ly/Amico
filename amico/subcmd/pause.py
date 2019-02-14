
import threading, time
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):

    def parse(self,cmdname,args,spiders):
        argv = args[0]
        if argv == 'spiders':
            return '\r\n Not a valid usage of command: pause <spider name>'
        d = {i.name:i for i in spiders}
        if argv in d:
            spider = d[argv]
            if spider.status == 'PAUSE':
                return f"* Spider {argv} hab been paused at {spider._pause_at} already. "
            elif spider.status == 'RUNNING' or \
                 spider.status == 'RESUME':
                lock = threading.Lock()
                lock.acquire()
                spider.status = 'PAUSE'
                spider._pause_at = time.ctime()
                lock.release()
                return f'* {spider._pause_at} Spider {argv} paused successfully. '
            else:
                return f'* Invalid pausing status "{spider.status}" for a spider. '
        else:
            return f'* No spider "{argv}" in the project.'
