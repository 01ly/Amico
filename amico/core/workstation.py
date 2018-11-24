#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import logging
from amico.core.serverthread import SpiderServer
from amico.core.spiderhub import SpiderHub
from amico.core.loader import SpiderLoader
from amico.core.crawler import WebCrawler
from amico.core.looper import Looper
from amico.middlewares import MiddleWareManager
from amico.log import install_root_logger
import time


logger = logging.getLogger(__name__)

class WorkStation(object):

    def __init__(self,settings):
        self.settings = settings
        self.spider_loader = SpiderLoader(settings)
        self.spiders = self.spider_loader.load_all_spiders()
        self.mw_manager = MiddleWareManager(self.spiders)
        self.crawler = WebCrawler(settings)
        self.looper = Looper()
        self.spider_hub = SpiderHub(settings,self.crawler)
        install_root_logger(settings)
        print(logging.root.handlers)
        # self.data_processor = DataProcessor(settings)
        logger.info('start')

    def _print_tips(self,got=True):
        print(f'* Amico - project : {self.settings["project"].PROJECT_NAME}')
        if got:
            print(f'* Running at {time.ctime()}')
            print(f'* Spiders inside the project: {[i.name for i in self.spiders]}')
        else:
            print('* No spiders inside the project yet.Try to create one!')
            print('* You can create a spider by using commands like:\n')
            print('>> amico cspider myspider\n')
            print('* Then you will see a directory named "myspider" ')
            print(f'* under the "spiders" folder of the project "{self.settings["project"].PROJECT_NAME}".')
            print('* What you need to do is edit the spider.py to perform as you want.')

    def work(self,excludes=None,spider_names=None):
        if excludes:
            spiders = [i for i in self.spiders if i.name not in excludes]
        elif spider_names:
            spiders = [i for i in self.spiders if i.name in spider_names]
        else:
            spiders = self.spiders
        if not spiders:
            self._print_tips(False)
            return
        else:
            self._print_tips()
            self.server = SpiderServer(self.settings,spiders)
            self.server.start()
        self.spider_hub.takeover(spiders)
        exported_req = self.spider_hub._gen_start_requests(looper=self.looper)
        self.crawler.convert(exported_req)
        self.looper.run_forever()
        self._close(spiders)

    def _close(self,spiders):
        for i in spiders:
            i.status = 'CLOSED'
            i.conn.close()

def test_hub(_ctrl):
    while 1:
        if _ctrl != 'STOP':
            for i in _ctrl:
                if isinstance(i,float):continue
                print(i.name,i.status)
            _ctrl.append(time.time())
            time.sleep(4)
        else:
            print(_ctrl)
            return
