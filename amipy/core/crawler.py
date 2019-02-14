#coding:utf-8

import asyncio
from amipy.BaseClass import Crawler,CrawlRequester
from amipy.cmd import _iter_specify_classes
from amipy.middlewares import MiddleWareManager
from amipy.log import getLogger

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
        self.logger = getLogger(__name__)
        self.semaphore = asyncio.Semaphore(
            self.settings['project'].CONCURRENCY)
        self._install_requester()

    def _install_requester(self):
        _cls = {}
        _module = self.settings['project'].CRAWLING_REQUESTER_MODULE
        for cls in _iter_specify_classes(_module,CrawlRequester):
            cls._crawler = self
            _cls[cls._down_type]=cls()
            self.logger.debug(f'Installed requester "{cls.__name__}".')
        self.requesters = _cls

    @MiddleWareManager.handle_req
    def convert(self,requests):
        self.logger.debug(f'Received {len(requests)} Requests.')
        tasks = []
        for req in requests:
            coro = self.requesters[req.down_type].crawl(req)
            task = asyncio.ensure_future(coro)
            task.add_done_callback(req.delegate_func)
            tasks.append(task)
        self.tasks.extend(tasks)
        self.logger.debug(f'Converted {len(tasks)} Tasks.')
        return tasks

    @property
    def runing_tasks(self):
        return [i for i in self.tasks if not i.done()]

    @property
    def finished_tasks(self):
        return [i for i in self.tasks if i.done()]



