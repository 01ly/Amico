#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import amico
import logging
from amico.BaseClass import Hub
from amico.middlewares import MiddleWareManager
from amico.util.filter import _to_feature

logger = logging.getLogger('amico')

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
        self._crawler = crawler

    def _gen_start_requests(self,looper):
        self.looper = looper
        coroutines = [i._generate_seed_requests() for i in self.spiders]
        requests = looper.run_coroutine(coroutines)
        if any(i for i in requests):
            _res = []
            [_res.extend(i) for i in requests]
            self.active = True
            return _res
        else:
            import sys
            print('*[End] No seed urls to start the spiders.')
            sys.exit(0)

    def takeover(self,spiders):
        self.spiders =spiders
        logger.info('Take:%s'%spiders)
        self._binding()

    def accept(self,request):
        _all_req = []
        if isinstance(request,list):
            for req in request:
                if not isinstance(req, amico.Request):
                   continue
                else:
                    _all_req.append(req)
        elif isinstance(request,amico.Request):
            _all_req.append(request)
        return _all_req

    @MiddleWareManager.handle_resp
    def delegate(self,response):
        _res = []
        if response.status == 200:
            self._success_counter += 1
            response.spider._success += 1
            a = self.accept(response.callback(response))
        elif response.status == -1:
            self._exception_counter += 1
            response.spider._exc +=1
            response.spider.urlfilter.delete(_to_feature(response.request))
            a = self.accept(response.excback(response))
        else:
            self._failed_counter += 1
            response.spider._fail += 1
            response.spider.urlfilter.delete(_to_feature(response.request))
            a = self.accept(response.errback(response))
        _res.extend(a)
        self._crawler.convert(_res)

    def __str__(self):
        return f'<SpiderHub obj at {hex(id(self))} active:{self.active}' \
               f' [spiders:{len(self.spiders)} success:{self._success_counter} ' \
               f'fail:{self._failed_counter} exc:{self._exception_counter}]>'
