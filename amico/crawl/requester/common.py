import asyncio
from amico import Response
from amico.BaseClass import CrawlRequester

class CommonRequester(CrawlRequester):

    _down_type = 'text/pic'

    async def crawl(self,request):
        url = request.url
        spider = request.spider
        delay = request.delay
        session = spider.session
        timeout = request.timeout
        try:
            async with self._crawler.semaphore:
                async with session.get(url,timeout=timeout) as resp:
                    res = await resp.read()
                    code = resp.status
                    await asyncio.sleep(delay)
            return Response(url=url,status=code,request=request, body=res)
        except asyncio.CancelledError:
            print(f'Task "{request}" canceled.')
            return Response(url, status=0, request=request)
        except Exception as e:
            return Response(url, status=-1, request=request, exc=e.__class__())

