import amipy
from w3lib.url import parse_url
from amipy.middlewares import Middleware
from amipy.log import getLogger
from urllib import robotparser
from amipy.exceptions import DropRequest

class RobotstxtMiddleware(Middleware):

    def __init__(self):
        self.rparser = {}
        self.rubbish = set()
        self.logger = getLogger(__name__)

    def process_request(self,request):
        spider = request.spider
        if  not request.obey_robots_txt:
            if not spider.settings.ROBOTS_TXT_OBEY:
                return request
        _purl = parse_url(request.url)
        netloc = _purl.netloc
        if not netloc in self.rparser :
            if netloc in self.rubbish:
                return request
            robots_url = f"{_purl.scheme}://{netloc}/robots.txt"
            req = amipy.Request(spider, robots_url)
            crawler = spider.binding_hub._crawler
            looper = spider.binding_hub.looper
            coro = crawler.requesters[req.down_type].crawl(req)
            resp = looper.run_coroutine(coro)
            if resp.status != 200:
                self.logger.debug(f'[{resp.status}] There is no robots.txt for "{netloc}".')
                self.rubbish.add(netloc)
                return request
            else:
                self.logger.debug(f'[{resp.status}] Found robots.txt for "{netloc}".')
                _parser = robotparser.RobotFileParser(robots_url)
                _parser.parse(resp.text().splitlines())
                self.rparser[netloc] = _parser
        else:
            _parser = self.rparser[netloc]
        ua = spider.settings.ROBOTS_USER_AGENT
        if _parser.can_fetch(ua,request.url):
            return request
        else:
            self.logger.debug(f'Forbidden by robots.txt of "{netloc}".'
                              f'Request:{request}')
            raise DropRequest






