#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import time
import re as _re
import w3lib.url as urltool

class BaseSpider(object):

    name = None
    binding_hub = None
    settings = None
    priority = 0
    urls = []
    my_settings = {}
    whitelist = []
    blacklist = []
    rules = []
    _start_at = time.ctime()
    _pause_at = None
    _resume_at = None
    _stop_at = None
    _success = 0
    _fail = 0
    _exc = 0
    urlfilter = None
    respfilter = None
    _hanged = set()

    def parse(self,response):
        '''Callback function to handle the success response'''
        raise NotImplementedError

    def error(self,response):
        '''Callback function to handle the status code of response that is not 200'''
        pass

    def exception(self,response):
        '''Callback function to handle the exception of response'''
        req = response.request
        exc = response.exception
        print(f'*[Exception:{self.name}] {exc.__class__.__name__}({exc}) '
              f'at:{req.method} - {req.url}')

    def fingerprint(self,response):
        '''indicate the base filter content to differ website pages'''
        return Fingerprint(None)

    def send(self,request):
        '''Send a Request to the binding SpiderHub'''
        raise NotImplementedError

    def start_requests(self):
        '''Generate the starting Requests for the spider.'''
        raise NotImplementedError

    def __gt__(self, other):
        return self.priority < other.priority


class Hub(object):

    spiders = []
    priorities = 0

    def accept(self,request):
        '''accept a Request from a spider.'''
        raise NotImplementedError

    def export(self):
        '''export Request objects from the hub.'''
        raise NotImplementedError

    def takeover(self,spiders):
        '''take over spiders but not binding yet.'''
        raise NotImplementedError

    def delegate(self,future):
        '''a delegate callback function when WebCrawler finished handling a Request.'''
        raise NotImplementedError

    def _binding(self):
        '''bind each spider to the hub'''
        for spider in self.spiders:
            spider.binding_hub = self
            spider.status = 'BOUND'
            self.priorities += spider.priority


class Crawler(object):

    def convert(self,requests):
        '''convert a Request list to a Task list'''
        raise NotImplementedError


class Url(object):
    '''an url identifier'''
    def __init__(self,url=None,re=None,domain=None,
                 path=None,params=None,query=None,
                 fragment=None,callback=None,
                 unmatch=None,drop=False,
                 filter=None,fingerprint=None):
        self._url = url
        self.path = path
        self.params = params
        self.query = query
        self.fragment = fragment
        self.pattern = _re.compile(re) if re else re
        self.domain = domain
        self.drop = drop
        self.cb = callback
        self.unmatch = unmatch
        self.filter = filter
        self.fingerprint = fingerprint

    @property
    def url(self):
        if self._url is None:
            return
        return urltool.canonicalize_url(
            urltool.safe_download_url(self._url)
            , encoding='utf-8')

    @url.setter
    def url(self,v):
        from amico.exceptions import Forbidden
        raise Forbidden('Setting url of an Url is forbidden.')

    def match(self,url):
        _m = None
        if self.pattern:
            _m = self.pattern.findall(url)
        parsed_url = urltool.parse_url(url)
        if (_m and _m[0] == url) or \
            url == self.url or \
            parsed_url.path == self.path or \
            parsed_url.query == self.query or \
            parsed_url.params == self.params or \
            parsed_url.netloc == self.domain or \
            parsed_url.fragment == self.fragment:
            return url

class Command(object):
    '''A console side commands recognition class'''
    requires_project = False
    parser  = None
    name = None

    def __init__(self,parser,name):
        self.parser = parser
        self.name = name

    def syntax(self):
        '''commands syntax (preferably one-line). Do not include commands name'''
        raise NotImplementedError

    def short_desc(self):
        '''a short description of the command'''
        raise NotImplementedError

    def long_desc(self):
        '''a long description of the command'''
        pass

    def add_options(self,parser):
        pass

    def help(self):
        '''shows the usage of this command.'''
        pass

    def handle(self,settings,opts, args):
        '''handle the command with the args and determine where to go'''
        raise NotImplementedError

    def run(self,settings):
        '''run the command'''
        raise NotImplementedError

class SpiderClientCommand(object):
    '''the base class of spider server commands tools at client side.'''

    def parse(self,cmdname,args,spiders):
        '''return the cmd parsed result'''
        raise NotImplementedError


class CrawlRequester(object):
    '''the base class of sending Requests generated by different kinds of spiders'''
    _down_type = None
    _crawler = None

    def crawl(self,request):
        '''defines how to deal with Requests'''
        raise NotImplementedError

class Middleware(object):
    '''identifies the middlewares'''

    def process_request(self,request):
        return request

    def process_response(self,response):
        return response


class Fingerprint(object):

    def __init__(self,text,precise=False):
        self.text = text
        self.precise = precise


