
from amico.exceptions import DropRequest
from amico.middlewares import Middleware

class ServerCtrlMiddleware(Middleware):

    def process_request(self,request):
        s = request.spider
        if s.status == 'PAUSE':
            s._hanged.add(request)
            raise DropRequest
        elif s.status == 'RUNNING':
            return request
        elif s.status == 'STOP':
            if any(s._hanged):
                raise DropRequest
            else:
                s._hanged.add(request)
                raise DropRequest