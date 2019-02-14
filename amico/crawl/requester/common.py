import asyncio
from amico import Response
from amico.BaseClass import CrawlRequester
from amico.util.http import send_async_http

class CommonRequester(CrawlRequester):

    _down_type = 'text/html'

    async def crawl(self,request):
        delay = request.delay
        url = request.url
        session = request.session
        try:
            async with self._crawler.semaphore:
                resp = await send_async_http(session,
                                            request.method,
                                            url,
                                            timeout=request.timeout,
                                            headers=request.headers,
                                            params=request.params,
                                            data=request.data,
                                            retries=request.retry,
                                            proxy=request.proxy)
                _resp = resp['resp']
                body = resp['body']
                exception = resp['exception']
                if exception:
                    return Response(url, status=-1, request=request, exc=exception)
            await asyncio.sleep(delay)
            return Response(url,request=request,body=body,_resp=_resp)
        except asyncio.CancelledError:
            print(f'Task "{request}" canceled.')
            return Response(url, status=0, request=request)
        except Exception as e:
            return Response(url, status=-1, request=request, exc=e.__class__())