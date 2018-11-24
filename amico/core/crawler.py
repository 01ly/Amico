#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-17
'''
import asyncio
from amico.BaseClass import Crawler,CrawlRequester
from amico.cmd import _iter_specify_classes
from amico.middlewares import MiddleWareManager

class WebCrawler(Crawler):

    tasks = []
    mw_manager = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(WebCrawler, cls).__new__(cls)
        return cls._instance

    def __init__(self,settings):
        super(WebCrawler,self).__init__()
        self.settings = settings
        self.semaphore = asyncio.Semaphore(self.settings['project'].CONCURRENCY)
        self._install_requester()

    def _install_requester(self):
        _cls = {}
        _module = self.settings['project'].CRAWLING_REQUESTER_MODULE
        for cls in _iter_specify_classes(_module,CrawlRequester):
            cls._crawler = self
            _cls[cls._down_type]=cls()
        self.requesters = _cls

    @MiddleWareManager.handle_req
    def convert(self,requests):
        for req in requests:
            coro = self.requesters[req.down_type].crawl(req)
            task = asyncio.ensure_future(coro)
            task.add_done_callback(req.delegate_func)
            self.tasks.append(task)

    @property
    def runing_tasks(self):
        return [i for i in self.tasks if not i.done()]

    @property
    def finished_tasks(self):
        return [i for i in self.tasks if i.done()]



