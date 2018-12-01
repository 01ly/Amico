
from amico.util.filter import _to_md5,_to_feature
from amico.middlewares import Middleware
from amico.exceptions import DropRequest,DropResponse
from amico.BaseClass import Fingerprint


class CrawlFilterMiddleware(Middleware):

    def process_request(self,request):
        spider = request.spider
        url = request.url
        _flag = self._rules_effect(url,spider)
        if _flag is None:
            if  not request.filter:
                return request
        elif not _flag:
            return request
        _filter = spider.urlfilter
        _feature = _to_feature(request)
        if _feature in _filter:
            raise DropRequest
        # else:
        #     _filter.add(_feature)
        return request

    def _rules_effect(self,url,spider,mode=0):
        rules = spider.rules
        for URL in rules:
            if URL.match(url):
                if mode==0:
                    if URL.filter != None:
                        return bool(URL.filter)
                else:
                    URL_FP =  URL.fingerprint
                    if isinstance(URL_FP,bool):
                        return URL_FP
                    if URL_FP != None and \
                        callable(getattr(spider,URL_FP,False)):
                        return getattr(spider,URL_FP)
        return None

    def process_response(self,response):
        url = response.url
        spider = response.spider
        spider.urlfilter.add(_to_feature(response.request))
        _flag = self._rules_effect(url,spider,1)
        if _flag is None:
            if not response.resp_filter:
                return response
        elif not _flag:
            return response
        if callable(response.fingerprint):
            _func = response.fingerprint if \
                not callable(_flag) else _flag
        elif isinstance(response.fingerprint,str) and \
                callable(getattr(spider,response.fingerprint)):
            _func = getattr(spider,response.fingerprint)
        else:
            raise ValueError('Not a valid fingerprint.')

        # fingerprint = _func(response)
        # if fingerprint.text is None or \
        #         not isinstance(fingerprint,Fingerprint):
        #     _fingerprint = response.text()
        # else:
        #     _fingerprint = fingerprint.text
        # if fingerprint.precise:
        #     _feature = _to_md5(_fingerprint)
        # else:
        #     _feature = _to_md5(_fingerprint)
        # if _feature in spider.respfilter:
        #     raise DropResponse
        # else:
        #     spider.respfilter.add(_feature)
        return response

    def _to_analyse(self,fingerprint):
        if len(fingerprint)<180:
            _feature = _to_md5(fingerprint)
            return _feature


    # def _extract_content(self,text):
