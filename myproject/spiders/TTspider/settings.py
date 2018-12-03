

NAME = 'linkin'

PATH = r'D:\CODE\Amico\mypro\spiders\TTspider'

# The filter error rate
BLOOMFILTER_ERROR_RATE = 0.0001
# The filter initial capacity
BLOOMFILTER_INITIAL_CAPACITY = 10**5

BLOOMFILTER_URL_ON = True
BLOOMFILTER_HTML_ON = False

BLOOMFILTER_URL_LOAD_PATH = r''
BLOOMFILTER_URL_SAVE_PATH = r'D:\\url_record.info'

BLOOMFILTER_HTML_LOAD_PATH = r''
BLOOMFILTER_HTML_SAVE_PATH = r'D:\\site_record.info'

CONCURRENCY = 60

MIDDLEWARE_TO_INSTALL = {
    'request':
    {
        #place your custom request handling middleware of the spider  here
        #e.g. <middleware module path>:<priority>
    },
    'response':
    {
        # place your custom response handling middleware of the spider here
        # e.g. <middleware module path>:<priority>
    },
    'both':
    {
        # place your custom middleware(both on request and response) of the spider here
        # e.g. <middleware module path>:<priority>
    }
}

REQUEST_DELAY = 5

REQUEST_TIMEOUT = 30

REQUEST_RETRY = 0

REQUEST_HEADERS = {
    'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}

#Default dowmload type of the spider
DEFAULT_DOWNLOAD_TYPE = 'text/pic'

SPIDER_COOKIES_UNSAFE_MODE = False
SPIDER_COOKIES_FOR_HEADERS = ''
SPIDER_COOKIES_CUSTOM ={}
SPIDER_COOKIES_LOAD_PATH =  r'D:\cookies.info'
SPIDER_COOKIES_SAVE_PATH =  r'D:\cookies.info'

