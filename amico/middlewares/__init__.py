
from functools import wraps
from amico.BaseClass import Middleware
from amico.cmd import _iter_specify_classes
from amico.exceptions import DropRequest

class MiddleWareManager(object):

    mw = {}
    req_mw = {}
    resp_mw = {}

    def __init__(self,spiders):
        self.spiders = spiders
        self._attrs = ('mw','resp_mw','req_mw')
        self.load_middlewares()

    def load_middlewares(self):
        _req_mw = {}
        _resp_mw = {}
        for spider in self.spiders:
            self.mw[spider.name] = spider.settings.MIDDLEWARE_TO_INSTALL
            _req_mw[spider.name] = self.mw[spider.name]['request']
            _resp_mw[spider.name] = self.mw[spider.name]['response']

        def _load( name_dict):
            mws = {}
            for name,modules in name_dict.items():
                mws[name]=[]
                for i in sorted(modules, key=lambda x: -modules[x]):
                    for j in _iter_specify_classes(i, Middleware):
                        mws[name].append(j())
            return mws

        self.req_mw = _load(_req_mw)
        self.resp_mw = _load(_resp_mw)
        [setattr(self.__class__, i,
                 self.__getattribute__(i)) for i in self._attrs]

    @classmethod
    def _process_request(cls,request):
        for i in cls.req_mw[request.spider.name]:
            try:
                request = i.process_request(request)
            except DropRequest:
                return None
        return request

    @classmethod
    def handle_req(cls,func):
        @wraps(func)
        def wrap(_self,requests,*args,**kwargs):
            _r = []
            if not any(requests):return None
            for req in sorted(requests,key=lambda x:-x.priority):
                request = cls._process_request(req)
                _r.append(request)
            if not any(_r):return None
            requests = [i for i in _r if i]
            return func(_self,requests,*args,**kwargs)
        return wrap