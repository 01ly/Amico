
from amico.middlewares import Middleware
from amico.exceptions import DropRequest
from amico import Url

class RulesHandleMiddleware(Middleware):

    def process_request(self,request):
        spider = request.spider
        url = request.url
        rules = [i for i in spider.rules if isinstance(i,Url)]
        for U in rules:
            if U.match(url):
                if U.drop:
                    raise DropRequest
                if U.cookies:
                    request._load_cookies(U.cookies)
                if U.cb:
                    cb = getattr(spider,U.cb,None)
                    if callable(cb):
                        request.callback = cb
                if bool(U.obey_robots_txt):
                    request.obey_robots_txt = True
                elif U.obey_robots_txt == False:
                    request.obey_robots_txt = False
                if U.down_type != None:
                    request.down_type = U.down_type
                if U.proxy != None:
                    request.proxy = U.proxy
                if U.proxy_auth != None:
                    request.proxy_auth = U.proxy_auth
                break
            else:
                if U.unmatch is None:
                    continue
                cb = getattr(spider,U.unmatch,None)
                if callable(cb):
                    request.callback = cb
        return request