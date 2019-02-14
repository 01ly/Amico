#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import amipy
from amipy.BaseClass import Hub
from amipy.middlewares import MiddleWareManager
from amipy.util.load import load_py
from amipy.log import getLogger

class SpiderHub(Hub):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(SpiderHub, cls).__new__(cls)
        return cls._instance

    def __init__(self,settings,crawler):
        super(SpiderHub, self).__init__()
        self.settings = settings
        self._success_counter = 0
        self._failed_counter = 0
        self._exception_counter = 0
        self.active = False
        self.looper = None
        self._crawler = crawler
        self.logger = getLogger(__name__)
        self._set_queue()

    def _set_queue(self):
        _queue = self.settings.gets('PROJECT_REQUESTS_QUEUE')
        self.requests = load_py(_queue)()
        self.logger.debug(f'Loaded Requests Queue:{type(self.requests).__name__}')

    def start(self,looper):
        self.looper = looper
        self.active = True
        for i in self.spiders:
            for seed in i.start_requests():
                i.status = 'RUNNING'
                if isinstance(seed, amipy.Request):
                    self.requests.put_nowait(seed)
        if self.requests.empty():
            print(f'* No start requests.Shutting down Amipy.\r\n')
            raise StopAsyncIteration
        self.logger.info(f'Got {self.requests.qsize()} start requests.')

    def takeover(self,spiders):
        self.spiders =spiders
        self.logger.debug(f'Takeover:{[i.name+":"+i.__class__.__name__ for i in spiders]}')
        self._binding()

    def _binding(self):
        for spider in self.spiders:
            spider.binding_hub = self
            spider.status = 'BOUND'
            self.priorities += spider.priority

    def accept(self,request):
        _all_req = []
        if isinstance(request,list):
            for req in request:
                if not isinstance(req, amipy.Request):
                   continue
                else:
                    _all_req.append(req)
        elif isinstance(request, amipy.Request):
            _all_req.append(request)
        return _all_req

    @MiddleWareManager.handle_resp
    def delegate(self,response):
        _res = []
        req = response.request
        spider = response.spider
        if response.status == 200:
            self._success_counter += 1
            spider._success += 1
            self.logger.info(f'[Success]{spider.name} {req.method}-{req.url}')
            a = self.accept(response.callback(response))
        elif response.status == -1:
            self._exception_counter += 1
            spider._exc +=1
            self.logger.info(f'[{response.exception.__class__.__name__}] {spider.name}'
                             f' {req.method}-{req.url} ')
            a = self.accept(response.excback(response))
        else:
            self._failed_counter += 1
            spider._fail += 1
            self.logger.info(f'[{response.status} Error]{spider.name} {req.method}-{req.url}')
            a = self.accept(response.errback(response))
        _res.extend(a)
        [self.requests.put_nowait(i) for i in _res if i]

    def __str__(self):
        return f'<SpiderHub obj at {hex(id(self))} active:{self.active}' \
               f' [spiders:{len(self.spiders)} success:{self._success_counter} ' \
               f'fail:{self._failed_counter} exc:{self._exception_counter}]>'
