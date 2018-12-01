

NAME = 'linkin'

PATH = r'D:\CODE\Amico\mypro\spiders\TTspider'

# Spider's BloomFilter ERROR_RATE is necessary
BLOOMFILTER_ERROR_RATE = 0.0001


CONCURRENCY = 60

MIDDLEWARE_TO_INSTALL = {
    'request':
    {
        'amico.middlewares.requestwares.ListHandle' : 1000,
        'amico.middlewares.requestwares.Rules'      : 1000,
        'amico.middlewares.requestwares.ServerCtrl' : 700,
        # 'amico.middlewares.CrawlFilter': 900,
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

REQUEST_DELAY = 5

REQUEST_TIMEOUT = 30

REQUEST_RETRY = 0

#Default dowmload type of the spider
DEFAULT_DOWNLOAD_TYPE = 'text/pic'


FILTER_URL_TAKE = True
FILTER_RESPONSE_TAKE = True