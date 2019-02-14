
from functools import wraps
from amipy.BaseClass import Middleware
from amipy.cmd import _iter_specify_classes
from amipy.exceptions import DropRequest,DropResponse
from amipy.log import getLogger

class MiddleWareManager(object):

    mw = {}
    req_mw = {}
    resp_mw = {}
    logger = None

    def __init__(self,settings,spiders):
        self._settings = settings
        self.spiders = spiders
        self._attrs = ('mw','resp_mw','req_mw')
        self.logger = getLogger(__name__)
        MiddleWareManager.logger = self.logger
        self.load_middlewares()

    def load_middlewares(self):
        _req_mw = {}
        _resp_mw = {}
        common_req_mw = self._settings['project'].MIDDLEWARE_COMMON_INSTALL['request']
        common_resp_mw = self._settings['project'].MIDDLEWARE_COMMON_INSTALL['response']
        common_both_mw = self._settings['project'].MIDDLEWARE_COMMON_INSTALL['both']
        for spider in self.spiders:
            self.mw[spider.name] = spider.settings.MIDDLEWARE_TO_INSTALL
            common_req_mw.update(self.mw[spider.name]['request'])
            common_resp_mw.update(self.mw[spider.name]['response'])
            common_both_mw.update( self.mw[spider.name]['both'])
            _req_mw[spider.name] = common_req_mw
            _resp_mw[spider.name] = common_resp_mw
            _req_mw[spider.name].update(common_both_mw)
            _resp_mw[spider.name].update(common_both_mw)

        def _load(name_dict):
            mws = {}
            for name,modules in name_dict.items():
                mws[name]=[]
                for i in sorted(modules, key=lambda x: -modules[x]):
                    for j in _iter_specify_classes(i, Middleware):
                        mws[name].append(j())
                        self.logger.debug(f'Loaded middleware [{name}] "{j.__name__}".')
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
                # cls.logger.debug(f'{i.__class__.__name__} Dropped '
                #                  f'[{request.spider.name}]-{request.method} {request.url}')
                return None
        return request

    @classmethod
    def _process_response(cls,future):
        response = future.result()
        if not response:
            return None
        if response.request._ignore:
            return response
        for i in cls.resp_mw[response.spider.name]:
            try:
                response = i.process_response(response)
            except DropResponse:
                # cls.logger.debug(f'{i.__class__.__name__} Dropped '
                #                  f'[{response.spider.name}]-[{response.status}] {response.url}')
                return None
        return response

    @classmethod
    def handle_req(cls,func):
        @wraps(func)
        def wrap(_self,requests,*args,**kwargs):
            if not any(requests):return None
            _r = []
            cls.logger.debug(f'Before Middleware handling:{len(requests)} Requests.')
            for req in sorted(requests,key=lambda x:-x.priority):
                if req._ignore:
                    _r.append(req)
                    continue
                request = cls._process_request(req)
                if isinstance(request,list):
                    _r.extend(request)
                else:
                    _r.append(request)
            if not any(_r):return None
            requests = [i for i in _r if i]
            cls.logger.debug(f'After Middleware handling:{len(requests)} Requests.')
            return func(_self,requests,*args,**kwargs)
        return wrap

    @classmethod
    def handle_resp(cls,func):
        @wraps(func)
        def wrap(_self, future, *args, **kwargs):
            response = cls._process_response(future)
            if response is None:
                return
            return func(_self, response, *args, **kwargs)
        return wrap