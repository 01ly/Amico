
from amico.middlewares import Middleware

class HeadersMiddleware(Middleware):

    def process_request(self,request):
        spider = request.spider
        headers = request.headers
        _header_cookies = spider.settings.SPIDER_COOKIES_FOR_HEADERS \
        if getattr(spider.settings,'SPIDER_COOKIES_FOR_HEADERS',False) else None
        if headers is None:
            _headers = spider.settings.REQUEST_HEADERS
            request.headers = _headers
        if _header_cookies:
            request.headers['Cookie'] = _header_cookies
        if request.headers.get('Cookie',None) or request.headers.get('cookie',None):
            _c = request.headers.get('Cookie','')
            _c = _c if _c else request.headers.get('cookie','')
            _c = self._parse_cookie(_c)
            spider.session.cookie_jar.update_cookies(_c)
        return request

    def _parse_cookie(self,cookie_str):
        c_dict = {}
        for  i in cookie_str.split(';'):
            k,v = i.split('=')
            c_dict.update({k.strip():v.strip()})
        return c_dict