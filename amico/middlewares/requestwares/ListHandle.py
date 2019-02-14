
import w3lib.url  as urltool
from amico.middlewares import Middleware
from amico.exceptions import DropRequest
from amico import Url

class UrlListHandleMiddleware(Middleware):

    def process_request(self,request):
        spider = request.spider
        url = request.url
        blacklist = spider.blacklist
        whitelist = spider.whitelist
        if self._is_in(url,blacklist):
            raise DropRequest
        if any(whitelist) and not \
                self._is_in(url,whitelist):
            raise DropRequest
        return request

    def _is_in(self,_url,_list):

        def _tran(url):
            return urltool.canonicalize_url(
            urltool.safe_download_url(url), encoding='utf-8')

        for url in _list:
            if isinstance(url,Url):
                if url.match(_url):
                    return True
            elif _tran(url) == _url:
                return True