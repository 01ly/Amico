#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import time
from amico.core.serverthread import SpiderServer
from amico.core.spiderhub import SpiderHub
from amico.core.loader import SpiderLoader
from amico.core.crawler import WebCrawler
from amico.core.looper import Looper
from amico.core.scheduler import Scheduler
from amico.middlewares import MiddleWareManager
from amico.log import getLogger

logger = getLogger(__name__)

class WorkStation(object):

    def __init__(self,settings):
        self.settings = settings
        self.spider_loader = SpiderLoader(settings)
        self.spiders = self.spider_loader.load_all_spiders()
        self.crawler = WebCrawler(settings)
        self.scheduler = Scheduler(settings)
        self.looper = Looper()
        self.spider_hub = SpiderHub(settings,self.crawler)
        # self.data_processor = DataProcessor(settings)

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
            print('* What you need to do is "edit the spider.py" as you want.')
            self._close()

    def work(self,excludes=None,spider_names=None):
        logger.debug('Workstation running.')
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
            self.mw_manager = MiddleWareManager(self.settings, spiders)
            if self.settings['project'].SPIDER_SERVER_ENABLE:
                self.server = SpiderServer(self.settings,spiders)
                self.server.start()
                logger.debug('SpiderServer started.')
            else:
                print('* Press Ctrl+C to stop the crawling.\n')
        self.spider_hub.takeover(spiders)
        self.spider_hub.start()
        while 1:
            try:
                self.scheduler.spiders_monitor(spiders)
                self.scheduler.receive(self.spider_hub.requests)
                tasks = self.crawler.convert(self.scheduler.export())
                self.looper.run_tasks(tasks)
            except (StopAsyncIteration,KeyboardInterrupt):
                break
        self._close()
        logger.info('Amico had been shut down.')

    def _close(self):
        for i in self.spiders:
            if not i.closed:
                i.close()