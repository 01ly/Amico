
from amipy.exceptions import DropRequest,DropResponse
from amipy.middlewares import Middleware
from amipy.log import getLogger
from amipy.util.filter import _to_feature

class ServerCtrlMiddleware(Middleware):

    logger = getLogger(__name__)

    def process_request(self,request):
        s = request.spider
        if s.status == 'PAUSE':
            self.logger.debug(f'PAUSE {s.name} {request}')
            s._hanged.append(request)
            if s.urlfilter:
                s.urlfilter.delete(_to_feature(request))
            raise DropRequest
        elif s.status == 'RUNNING':
            return request
        elif s.status in ['STOP','CLOSE']:
            if s.urlfilter:
                s.urlfilter.delete(_to_feature(request))
            self.logger.debug(f'STOP/CLOSE {s.name} {request}')
            raise DropRequest

    def process_response(self,response):
        spider = response.spider
        if spider.status =='STOP':
            raise DropResponse
        return response