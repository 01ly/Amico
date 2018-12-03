

CONCURRENCY = 64

#Default dowmload type of the spider
DEFAULT_DOWNLOAD_TYPE = 'text/pic'

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
    },
    'both':
    {
        'amico.middlewares.CrawlFilter' : 900,
    }
}

REQUEST_DELAY = 2
REQUEST_RETRY = 0
REQUEST_TIMEOUT = 15


AUTH_USERNAME = ''
AUTH_PASSWORD = ''

REQUEST_HEADERS = {
    'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


