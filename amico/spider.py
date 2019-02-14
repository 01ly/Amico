#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import os
import amico
import aiohttp
import bloompy
from amico.util.filter import _generate_filter
from amico.core.spiderhub import SpiderHub
from amico.BaseClass import BaseSpider
from amico.log import getLogger

class Spider(BaseSpider):

    def __init__(self,*args,**kwargs):
        super(BaseSpider, self).__init__(*args,**kwargs)
        self.status = 'CREATED'
        self.requests = []
        self.session = None
        self.logger = getLogger(__name__)
        self._load_settings()
        self._load_filters()
        self._init_session()

    def __str__(self):
        return f'<{self.__class__.__name__}({self.name}) object' \
               f' at {hex(id(self))} success:{self._success} ' \
               f'fail:{self._fail} exc:{self._exc} {self.status}>'

    def start_requests(self,urls=None):
        urls = self.urls if not bool(urls) else urls
        return [amico.Request(self, url,ignore=True)  for url in urls]

    def _load_settings(self):
        from inspect import ismodule
        if not ismodule(self.settings):
            self.settings = type('s', (), self.my_settings)
        if self.my_settings:
            for key,value in self.my_settings.items():
                if key=='NAME':continue
                setattr(self.settings,key,value)

    def _load_filters(self):
        u_path = self.settings.BLOOMFILTER_URL_LOAD_PATH
        h_path = self.settings.BLOOMFILTER_HTML_LOAD_PATH
        if self.settings.BLOOMFILTER_URL_ON:
            if os.path.exists(u_path):
                self.urlfilter = bloompy.get_filter_fromfile(u_path)
            else:
                self.urlfilter = _generate_filter(self.settings)
            self.logger.debug(f'Loaded [{self.name}] urlfilter,'
                          f'count:{self.urlfilter.count},'
                          f'capacity:{self.urlfilter.capacity},'
                          f'error rate:{self.urlfilter.error_rate}')
        if self.settings.BLOOMFILTER_HTML_ON:
            if os.path.exists(h_path):
                self.respfilter = bloompy.get_filter_fromfile(h_path)
            else:
                self.respfilter = _generate_filter(self.settings)
            self.logger.debug(f'Loaded [{self.name}] respfilter,'
                              f'count:{self.respfilter.count},'
                              f'capacity:{self.respfilter.capacity},'
                              f'error rate:{self.respfilter.error_rate}')

    def _init_session(self):
        _safe = self.settings.SPIDER_COOKIES_UNSAFE_MODE
        path = self.settings.SPIDER_COOKIES_LOAD_PATH
        _c_cookies = self.settings.SPIDER_COOKIES_CUSTOM
        jar = aiohttp.CookieJar(unsafe=_safe)
        if _c_cookies:
            cookies = _c_cookies
        else:
            cookies = None
        self.conn = aiohttp.TCPConnector(limit=self.settings.CONCURRENCY)
        self.session = aiohttp.ClientSession(connector=self.conn,
                                             cookies=cookies,
                                             cookie_jar=jar)
        if path:
            if os.path.exists(path):
                try:
                    self.session.cookie_jar.load(path)
                    if cookies:
                        self.session.cookie_jar.update_cookies(cookies)
                except:
                    return
                self.logger.debug(f'Loaded [{self.name}] cookie jar.')

    @property
    def cookies(self):
        return self.session.cookie_jar._cookies

    @cookies.setter
    def cookies(self,_cookies):
        if isinstance(_cookies,dict):
            self.session.cookie_jar.update_cookies(_cookies)
        else:
            import warnings
            warnings.warn(f'Not a valid cookie type,expected Dict,'
                          f'got:{type(_cookies).__name__}')

    def send(self, request):
        if not isinstance(request, amico.Request):
            raise TypeError(f'not a valid Request to send,'
                            f'got "{type(request).__name__}".')
        if not isinstance(self.binding_hub,SpiderHub):
            raise TypeError('Not a valid binging SpiderHub for Spider %s,got "%s".'
                            %(self.name, type(self.binding_hub).__name__))
        self.binding_hub.requests.put_nowait(request)

    def save_cookies(self):
        path = self.settings.SPIDER_COOKIES_SAVE_PATH
        if path:
            try:
                self.session.cookie_jar.save(path)
            except:
                return
            self.logger.debug(f'Save cookies of "{self.name}" succeed.')

    def save_records(self):
        if self.settings.BLOOMFILTER_URL_ON:
            path = self.settings.BLOOMFILTER_URL_SAVE_PATH
            if path:
                self.urlfilter.tofile(path)
                self.logger.debug(f'Save urlfilter of "{self.name}" succeed.')
        if self.settings.BLOOMFILTER_HTML_ON:
            path = self.settings.BLOOMFILTER_HTML_SAVE_PATH
            if path:
                self.respfilter.tofile(path)
                self.logger.debug(f'Save respfilter of "{self.name}" succeed.')

    def close(self,save=True):
        if self.closed:
            return
        self.status = 'CLOSE'
        if save:
            self.save_cookies()
            self.save_records()
        self.conn.close()
        self.closed = True

    def resume(self):
        self.status = 'RUNNING'
        while self._hanged:
            a = self._hanged.pop(0)
            if a:
                self.logger.debug(f'RESUME {self.name} {a}')
                self.binding_hub.requests.put_nowait(a)

    def restart(self):
        self.status = 'RUNNING'
        self.stopped = False
        if self._meta.get('restart_urls'):
            urls = self._meta['restart_urls']
        else:
            urls = []
        req = self.start_requests(urls)
        self.logger.debug(f'RESTART {self.name} {req}')
        [self.binding_hub.requests.put_nowait(i) for i in req if i]