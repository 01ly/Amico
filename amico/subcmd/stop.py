
import threading, time
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):

    def parse(self,cmdname,args,spiders):
        argv = args[0]
        if argv == 'spiders':
            return '\r\n Not a valid usage of command: stop <spider name>'
        d = {i.name:i for i in spiders}
        if argv in d:
            spider = d[argv]
            if spider.status == 'STOP':
                return f"* Spider {argv} hab been stopped at {spider._stop_at} already. "
            else:
                lock = threading.Lock()
                lock.acquire()
                spider.status = 'STOP'
                spider._stop_at = time.ctime()
                lock.release()
                return f'* {spider._stop_at} Spider {argv} stopped successfully. '
        else:
            return f'* No spider "{argv}" in the project.'
