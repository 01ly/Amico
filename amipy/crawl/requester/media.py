import os
import asyncio
from amipy import Response
from amipy.BaseClass import CrawlRequester
from amipy.util.http import send_async_http
from amipy.util.file import get_file_size
from amipy.log import getLogger

class MediaRequester(CrawlRequester):

    _down_type = 'media'

    logger = getLogger(__name__)

    async def crawl(self,request):
        delay = request.delay
        url = request.url
        session = request.spider.session
        proxy = request.proxy
        buffer = request.spider.settings.DEFAULT_DOWNLOAD_BUFFER
        path = os.path.normpath(request.save_path)
        if not os.path.exists(os.path.dirname(path)):
            self.logger.error(f'No path:{os.path.dirname(path)}.')
            return
        name = os.path.basename(path)
        try:
            self.logger.info(f'Downloading {name}.')
            async with self._crawler.semaphore:
                resp = await send_async_http(   session,
                                                request.method,
                                                url,
                                                path=path,
                                                retries=request.retry,
                                                timeout=request.timeout,
                                                proxies=proxy,
                                                buffer=buffer
                                            )
                if resp is None:
                    return
                body = resp['body']
                exception = resp['exception']
                if exception and body != True:
                    return Response(url, status=-1, request=request, exc=exception)
            await asyncio.sleep(delay)
            size = get_file_size(size=int(resp['size']))
            self.logger.info(f'Finished downloading:[{name} {size}]')
            return
        except asyncio.CancelledError:
            print(f'Task "{request}" canceled.')
            return Response(url, status=0, request=request)
        except Exception as e:
            return Response(url, status=-1, request=request, exc=e.__class__())