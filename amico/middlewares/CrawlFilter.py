import re
import os
from amico.util.filter import _to_md5,_to_feature
from amico.middlewares import Middleware
from amico.exceptions import DropRequest,DropResponse
from amico.BaseClass import Fingerprint
from bs4 import BeautifulSoup as bs

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
        else:
            _filter.add(_feature)
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
        if response.status != 200 and spider.urlfilter:
            spider.urlfilter.delete(_to_feature(response.request))
        if response.status == -1:
            return response
        self.spider = spider
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
        fingerprint = _func(response)
        if fingerprint.text is None or \
                not isinstance(fingerprint,Fingerprint):
            _fingerprint = response.read()
        else:
            _fingerprint = fingerprint.text
        if fingerprint.precise:
            _feature = _to_md5(_fingerprint)
        else:
            _feature = self._to_analyse(_fingerprint,
                                        spider.settings.BLOOMFILTER_HTML_EXTRACTS)
        if _feature in spider.respfilter:
            raise DropResponse
        else:
            spider.respfilter.add(_feature)
        return response

    def _to_analyse(self,fingerprint,extract_list):
        if fingerprint is None:
            raise DropResponse
        if len(fingerprint)<180:
            return _to_md5(fingerprint)
        html = bs(fingerprint,'lxml')
        [i.extract() for j in extract_list  for i in html(j) ]
        _text = html.body.text
        text = re.sub('\n','',_text).replace('\r','')
        if len(text)<180:
            return _to_md5(fingerprint)
        lines_content = _text.splitlines()
        res_dict = self._extract_content(lines_content)
        if not res_dict:
            return _to_md5(text)
        else:
            keys = sorted(res_dict.keys(),key=lambda x:-x)[:2]
            texts =''.join([res_dict[i] for i in keys])
            return _to_md5(texts)

    def _extract_content(self,lines_content):
        gap = self.spider.settings.BLOOMFILTER_HTML_GAP
        threshold = self.spider.settings.BLOOMFILTER_HTML_THRESHOLD
        density = self.spider.settings.BLOOMFILTER_HTML_DENSITY
        results = {}
        comobo_num = 0
        combo_len = 0
        combo_null = 0
        combo_text = ''
        pre_len = 0
        for i in lines_content:
            if i.strip():
                pre_len = len(i)
                comobo_num += 1
                combo_null = 0
                combo_len += pre_len
                combo_text = combo_text + i + os.linesep
                if len(lines_content) == 1 and pre_len >= density * threshold:
                    results[pre_len] = combo_text
            else:
                combo_null += 1
                if pre_len:
                    if combo_null > gap:
                        if combo_len >= density * threshold \
                                and comobo_num >= threshold:
                            results[combo_len] = combo_text
                    else:
                        continue
                comobo_num = 0
                combo_len = 0 if combo_null > gap else combo_len
                pre_len = 0
                combo_text = '' if combo_null > gap else combo_text
        return results