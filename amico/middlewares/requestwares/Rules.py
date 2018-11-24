
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
                if U.cb is None:
                    continue
                cb = getattr(spider,U.cb,None)
                if U.drop:
                    raise DropRequest
                if callable(cb):
                    request.callback = cb
                    return request
            else:
                if U.unmatch is None:
                    continue
                cb = getattr(spider,U.unmatch,None)
                if callable(cb):
                    request.callback = cb
                    return request
        return request