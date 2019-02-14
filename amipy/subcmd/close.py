
import threading, time
from amipy.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):

    def parse(self,cmdname,args,spiders):
        argv = args[0]
        if argv == 'spiders':
            return '\r\n Not a valid usage of command: close <spider name>'
        d = {i.name:i for i in spiders}
        if argv in d:
            spider = d[argv]
            if spider.status == 'CLOSE':
                return f"* Spider {argv} hab been closed at {spider._close_at} already. "
            else:
                lock = threading.Lock()
                lock.acquire()
                spider.status = 'CLOSE'
                spider._close_at = time.ctime()
                lock.release()
                return f'* {spider._close_at} Spider {argv} closed successfully. '
        else:
            return f'* No spider "{argv}" in the project.'
