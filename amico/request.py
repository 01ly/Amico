#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''

import amico
import w3lib.url as urltool

class Request(object):
    def __init__(self,spider,url,*,
                 callback=None,
                 headers=None,
                 errback=None,
                 excback=None,
                 params=None,
                 kwargs_cb=None,
                 cookies=None,
                 data=None,
                 down_type=None,
                 encoding='utf-8',
                 method='GET',
                 filter=None,
                 fingerprint=None,
                 retry=0,
                 priority=0,
                 delay = 0,
                 timeout=None,
                 ):

        assert isinstance(spider,amico.Spider),\
            f'the Request should be bounded to a Spider,' \
            f'got "{type(spider).__name__}".'

        assert isinstance(kwargs_cb,dict) or kwargs_cb is  None,\
            'params from Request to success callback should be a dict.'

        callback = callback if callback else spider.parse
        errback = errback if errback else spider.error
        excback = excback if excback else spider.exception

        assert callback or kwargs_cb is not None,\
            'there is no callback function for the Request.'
        assert callable(callback),\
            f'callback should be a coroutine function ,' \
            f'got "{type(callback).__name__}".'
        assert callable(errback) or errback is None, \
            f'errback should be a coroutine function,' \
            f'got "{type(errback).__name__}".'
        assert callable(excback) or excback is None, \
            f'excback should be a coroutine function,' \
            f'got "{type(excback).__name__}" .'
        assert method.strip().upper() in \
               ('GET','POST','HEAD','PUT','DELETE','UPDATE'), \
            "the method of a Request should be one of " \
            "the ['GET','POST','HEAD','PUT','DELETE','UPDATE']. "

        self.spider = spider
        self.callback = callback
        self.errback = errback
        self.excback = excback
        self.encoding = encoding
        self.priority = priority
        self.method = method
        self.data = data
        self.params = params
        self.fingerprint = fingerprint
        self.headers = headers
        self._ignore = False
        self.filter  = bool(filter) if filter != None \
            else spider.settings.BLOOMFILTER_URL_ON
        self.kwargs_cb = {} if not kwargs_cb \
            else kwargs_cb
        self.down_type = down_type if down_type\
            else spider.settings.DEFAULT_DOWNLOAD_TYPE
        self.retry = retry if retry !=0 \
            else spider.settings.REQUEST_RETRY
        self.delay = delay if delay !=0 \
            else spider.settings.REQUEST_DELAY
        self.timeout = timeout if timeout is not None \
            else spider.settings.REQUEST_TIMEOUT

        self._set_url(url)
        self._set_delegate(spider.binding_hub.delegate)

    def _set_url(self,url):
        self.url = urltool.canonicalize_url(
            urltool.safe_download_url(url),encoding=self.encoding)

    def _set_delegate(self,func):
        self.delegate_func = func

    @property
    def delegate_func(self):
        return self._func

    @delegate_func.setter
    def delegate_func(self,func):
        if func is None:
            self._func = None
        elif not callable(func):
            raise TypeError('delegate func should be callable,got "%s".'\
                            %type(func).__name__)
        else:
            self._func = func

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self,url):
        #only starts with schema:file,http,https allowed to be a valid url
        if not urltool.is_url(url):
            raise ValueError('Not a valid url for Request.Got:%s'%url)
        else:
            self.__url = urltool.safe_download_url(url)

    def __str__(self):
        return '<Request obj at %s [ spider=%s url=%s ] >'\
               %(hex(id(self)),self.spider.name,self.url)

    def __gt__(self, other):
        return self.priority < other.priority and \
               self.spider > other.spider
