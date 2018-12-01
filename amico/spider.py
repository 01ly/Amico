#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import amico
import aiohttp
from amico.util.filter import _generate_filter
from amico.core.spiderhub import SpiderHub
from amico.BaseClass import BaseSpider

class Spider(BaseSpider):

    def __init__(self,*args,**kwargs):
        super(BaseSpider, self).__init__(*args,**kwargs)
        self.status = 'CREATED'
        self.requests = []
        self.session = None
        self._load_settings()
        self.urlfilter = _generate_filter(self.settings)
        self.respfilter =  _generate_filter(self.settings)
        self.conn = aiohttp.TCPConnector(limit=self.settings.CONCURRENCY)
        self.session = aiohttp.ClientSession(connector=self.conn)

    def __str__(self):
        return f'<{self.__class__.__name__}({self.name}) object' \
               f' at {hex(id(self))} success:{self._success} ' \
               f'fail:{self._fail} exc:{self._exc} {self.status}>'

    async def _generate_seed_requests(self):
        self.status = 'RUNNING'
        _req = self.start_requests()
        return _req

    def start_requests(self):
        _starts = []
        for url in self.urls:
            a = amico.Request(self, url)
            a._ignore = True
            _starts.append(a)
        return _starts

    def _load_settings(self):
        from inspect import ismodule
        if not ismodule(self.settings):
            self.settings = type('s', (), self.my_settings)
        if self.my_settings:
            for key,value in self.my_settings.items():
                if key=='NAME':continue
                setattr(self.settings,key,value)

    def send(self, request):
        if not isinstance(request, amico.Request):
            raise TypeError(f'not a valid Request to send,'
                            f'got "{type(request).__name__}".')
        if not isinstance(self.binding_hub,SpiderHub):
            raise TypeError('Not a valid binging SpiderHub for Spider %s,got "%s".'
                            %(self.name, type(self.binding_hub).__name__))
        _a = self.binding_hub.accept(request)
        self.binding_hub._crawler.convert(_a)

    async def resume(self):
        _resume = []
        self.status = 'RUNNING'
        if any(self._hanged):
            _resume.extend(self._hanged)
        else:
            _resume.extend([amico.Request(self,url) for url in self.urls])
        self.binding_hub._crawler.convert(_resume)