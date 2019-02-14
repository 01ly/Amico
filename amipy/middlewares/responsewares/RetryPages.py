from amipy.middlewares import Middleware
from asyncio import TimeoutError
from amipy.log import getLogger
from aiohttp.client_exceptions import ServerDisconnectedError,\
    ServerConnectionError,ClientOSError,ClientConnectionError

exceptions = [TimeoutError,ServerConnectionError,
              ServerDisconnectedError,ClientConnectionError,
              ClientOSError]

class RetryPagesMiddleware(Middleware):

    logger = getLogger(__name__)

    def process_response(self,response):
        spider = response.spider
        codes = spider.settings.REQUESTS_ERROR_RETRY_STATUS
        if spider.settings.REQUESTS_FAIL_RETRY_ENABLE:
            if response.status != 200:
                if (response.status in codes
                    and response.status != -1) or \
                    (response.exception.__class__ in exceptions):
                    _tried = response.request._tried
                    if _tried > spider.settings.REQUESTS_FAIL_RETRY_DEPTH:
                        return response
                    response.request._tried = _tried + 1
                    response.request.proxy=None
                    self.logger.debug(f'{response.request} scheduled to retry.Tried:{_tried}')
                    spider._retries.append(response.request)
        return response


