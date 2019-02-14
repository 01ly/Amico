
# The spider name.
NAME = ''
# Location of the spider in the system.
PATH = r''
# Error rate of the BloomFilter.
BLOOMFILTER_ERROR_RATE = 0.0001
# The initial capacity of the BloomFilter.
BLOOMFILTER_INITIAL_CAPACITY = 10**5
# Turn on the requests url filter mode.
BLOOMFILTER_URL_ON = True
# Turn on the websites content filter mode.
BLOOMFILTER_HTML_ON = True
# Load the specified/previous requests BloomFilter from the disk.
BLOOMFILTER_URL_LOAD_PATH = r''
# Save the current requests BloomFilter into a file.
BLOOMFILTER_URL_SAVE_PATH = r'url_record.info'
# Load the specified/previous content BloomFilter from the disk.
BLOOMFILTER_HTML_LOAD_PATH = r''
# Save the current content BloomFilter into a file.
BLOOMFILTER_HTML_SAVE_PATH = r'site_record.info'
# Extract some tags from the response content.
BLOOMFILTER_HTML_EXTRACTS = ['script','style','head']
# Combo allowed null strings in the target content.
BLOOMFILTER_HTML_GAP = 3
# The minimum continuation lines in the target content.
BLOOMFILTER_HTML_THRESHOLD = 5
# The number of words in a line of the target content.
BLOOMFILTER_HTML_DENSITY =45
# The max concurrency of the spider.
CONCURRENCY = 60
# Default mode of the crawler downloading module.
DEFAULT_DOWNLOAD_TYPE = 'text/html'
# Default downloading buffer size for the crawler under the media mode.
DEFAULT_DOWNLOAD_BUFFER = 1024*10
# MongoDB settings for data saving.
DATABASE_SETTINGS = {
    'host':'127.0.0.1',
    'port':27017,
    'user':'',
    'password':'',
    'database':'test',
}
# Proxy mode.
HTTP_PROXY_ENABLE = False
# If the specified proxy doesn't work,requesting a valid proxy instead.
HTTP_PROXY_FILL_ENABLE = True
# Specified the global proxy for all requests.
HTTP_PROXY = ''
# The proxy pool api for crawling.
HTTP_PROXY_API = ''
# The statuses should be treat as successful response status.
HTTP_PROXY_FAKE_STATUS = []
# Middleware for crawling.
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
# Delay when get a response.
REQUEST_DELAY = 3
# Timeout for each request.
REQUEST_TIMEOUT = 20
# Retry times for each common request.
REQUEST_RETRY = 3
# Retry gathered failed Requests when every Request had been sent.
REQUESTS_FAIL_RETRY_ENABLE = True
# Retry times.
REQUESTS_FAIL_RETRY_DEPTH = 3
# Which response status should be retry.
REQUESTS_ERROR_RETRY_STATUS = [544,500,]
# The request headers of each Request.
REQUEST_HEADERS = {
    'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}
# Obey the target website's robots.txt.
ROBOTS_TXT_OBEY = True
# The name of your spider bot.
ROBOTS_USER_AGENT = 'AmipyBot'
# Use unsafe cookies mode.
SPIDER_COOKIES_UNSAFE_MODE = False
# Cookies string in the request headers.
SPIDER_COOKIES_FOR_HEADERS = ''
# Dictionary cookies to push into our request headers.
SPIDER_COOKIES_CUSTOM ={}
# The disk locations where the previous cookie file lies.
SPIDER_COOKIES_LOAD_PATH =  r''
# Save the current cookies into a local disk file.
SPIDER_COOKIES_SAVE_PATH =  r'cookies.info'

