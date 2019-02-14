
import amipy
from amipy.middlewares import Middleware
from amipy.util.proxy import gen_proxy,\
    is_proxy_valid,extract_ip_port
from amipy.log import getLogger
from w3lib.url import parse_url,is_url

class HttpProxyMiddleware(Middleware):

    inited = False
    invalid_pool = {}
    proxy_pool = set()
    logger = getLogger(__name__)

    def _proxy_invalid(self,proxy,url):
        domain = parse_url(url).netloc
        if proxy in self.invalid_pool:
            if domain in self.invalid_pool[proxy]:
                return True
            return False

    def process_request(self,request):
        if not request.spider.settings.HTTP_PROXY_ENABLE:
            request.proxy = None
            return request
        _type = request.down_type
        proxy = request.proxy
        url = request.url
        if proxy:
            if not is_proxy_valid(proxy):
                if request.spider.settings.HTTP_PROXY_FILL_ENABLE:
                    request.proxy = self.get_proxy(request)
                    if request.proxy:
                        self.logger.warn(f'Filling a new proxy {request.proxy} to {url}.')
                else:
                    self.logger.error(f'Not a valid http proxy:{proxy}')
                    request.proxy = None
                return request
            elif self._proxy_invalid(proxy,url):
                    self.logger.warn(f'Proxy {proxy} is invalid for {url} before.')
                    if request.spider.settings.HTTP_PROXY_FILL_ENABLE:
                        request.proxy = self.get_proxy(request)
                        if request.proxy:
                            self.logger.warn(f'Filling a new proxy {request.proxy} to {url}.')
                    else:
                        self.logger.warn(f'Dropped proxy {proxy} for {url}.')
                        request.proxy = None
                    return request
            request.proxy = gen_proxy(proxy,_type)
            self.logger.debug(f'[{request.spider.name}]Using proxy {request.proxy} '
                              f'for {request.method}-{request.url}')
        else:
            _proxy = None
            while 1:
                _proxy = self.get_proxy(request)
                if _proxy is None:
                    break
                proxy = extract_ip_port(_proxy)
                if self._proxy_invalid(proxy,url):
                    continue
                break
            request.proxy = _proxy
        return request

    def process_response(self,response):
        settings = response.spider.settings
        fakes = settings.HTTP_PROXY_FAKE_STATUS
        domain = parse_url(response.url).netloc
        if not response.spider.settings.HTTP_PROXY_ENABLE:
            return response
        if response.request.proxy and response.status != 200 \
                and response.status not in fakes:
            proxy = extract_ip_port(response.request.proxy)
            if proxy not in self.invalid_pool:
                self.invalid_pool[proxy] = set()
            self.logger.debug(f'Proxy {proxy} is invalid for '
                             f'{domain}.')
            self.invalid_pool[proxy].add(domain)
        elif  response.request.proxy and (response.status == 200
                                          or response.status in fakes):
            proxy = extract_ip_port(response.request.proxy)
            if proxy in self.invalid_pool:
                self.invalid_pool[proxy].discard(domain)
            self.proxy_pool.add(proxy)
        return response

    def get_proxy(self,req):
        http_proxy = req.spider.settings.HTTP_PROXY
        if http_proxy:
            if is_proxy_valid(http_proxy):
                proxy =  gen_proxy(http_proxy,req.down_type)
                return proxy
            elif is_url(http_proxy):
                return http_proxy
            else:
                if not req.spider.settings.HTTP_PROXY_FILL_ENABLE:
                    self.logger.debug(f'Invalid proxy format:{http_proxy}')
                    return
        _proxy = self.get_proxy_by_api(req)
        proxy = gen_proxy(_proxy,req.down_type)
        return proxy


    def get_proxy_by_api(self,request):
        domain = parse_url(request.url).netloc
        def _get_from_pool():
            while self.proxy_pool:
                proxy = self.proxy_pool.pop()
                if proxy not in self.invalid_pool or\
                        (domain not in self.invalid_pool.get(proxy)):
                    return proxy
                else:
                    continue
        proxy = _get_from_pool()
        if not proxy:
            self.logger.debug(f'No proxy in proxy pool.Getting some.')
            while 1:
                spider = request.spider
                req = amipy.Request(spider, spider.settings.HTTP_PROXY_API, delay=0, ignore=True)
                crawler = spider.binding_hub._crawler
                looper = spider.binding_hub.looper
                coro = crawler.requesters[req.down_type].crawl(req)
                resp = looper.run_coroutine(coro)
                if not resp:
                    self.logger.error(f'[{resp.status}]Getting Http proxy by api failed.')
                    continue
                _results = [i.strip() for i in resp.text().split('\n')]
                results =  [is_proxy_valid(i)[0] for i in _results if is_proxy_valid(i)]
                self.proxy_pool.update(results)
                self.logger.debug(f'Got {len(results)} http proxies from HTTP_PROXY_API.')
                proxy = _get_from_pool()
                if not proxy:
                    continue
                break
        return proxy


