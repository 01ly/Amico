
from amico.middlewares import Middleware

class ServerCtrlMiddleware(Middleware):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(ServerCtrlMiddleware,
                                  cls).__new__(cls)
        return cls._instance

    _paused = {}

    @classmethod
    def process_request(cls,request):
        print(23333389)
        return request


