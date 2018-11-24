

NAME = 'linkin'

PATH = r'D:\CODE\Amico\mypro\spiders\TTspider'

CONCURRENCY = 60

MIDDLEWARE_TO_INSTALL = {
    'request':
    {
        'amico.middlewares.requestwares.ListHandle' : 1000,
        'amico.middlewares.requestwares.Rules'      : 800,
        'amico.middlewares.requestwares.ServerCtrl' : 700,
        #place your custom request handling middleware here
        #e.g. <middleware module path>:<priority>
    },
    'response':
    {
        # 'amico.middlewares.responsewares.decode':1000,

    }
}

REQUEST_DELAY = 2

REQUEST_TIMEOUT = 15

REQUEST_RETRY = 0

#Default dowmload type of the spider
DEFAULT_DOWNLOAD_TYPE = 'text/pic'

REQUESTS_SEND_ONCE = 200
