#coding:utf-8
import copy
import requests
import asyncio
from contextlib import closing

async def send_async_http(session,method,url,*,
                             retries=1,
                             interval=1,
                             wait_factor=2,
                             timeout=0,
                             path = None,
                             success_callback=None,
                             fail_callback=None,
                             **kwargs) -> dict:
    """
    Send an async http request and implement the retry mechanism.
    Once the requesting operation failed,it will delay a interval time
    for the next retry.
    :param session:asynchronous request session
    :param method:request method
    :param url:request url
    :param retries:how many it will retry
    :param interval:a delay interval secs.
    :param wait_factor:wait factor,every retry failed will multiply by it to delay for
    next retry,recommended 1<wf<2
    :param timeout:requesting timeout
    :param success_callback:callback for successes
    :param fail_callback:callback for fails
    :param kwargs:other kwargs
    :param path:file save path
    :return:result
    """
    ret = {'resp':None,'body':None,'code':-1,
           'exception':None,'tries':-1}
    wait_interval = interval
    if method.lower() not in ['get','head','post','put']:
        return ret
    if retries == -1:  # -1 means retry unlimited times
        attempt = -1
    elif retries == 0:  # 0 means no retry
        attempt = 1
    else:
        attempt = retries + 1
    while attempt != 0:
        size = 0
        try:
            if path:
                loop = asyncio.get_running_loop()
                try:
                    resp = await loop.run_in_executor(None,download,url,path,timeout,kwargs)
                    size = resp
                    body = True
                    code = 200
                except requests.exceptions.Timeout:
                    raise TimeoutError
            else:
                async with getattr(session,method.lower())(url,timeout=timeout,**kwargs) as response:
                    code = response.status
                    resp = response
                    body = await response.read()
            ret.update({'resp': resp, 'body':body,'code': code,
                        'tries': retries - attempt+1,'size':size})
            if success_callback:
                success_callback(ret)
            return ret
        except Exception as e:
            ret['exception'] = e.__class__()
            ret['tries'] += 1
            await asyncio.sleep(wait_interval)
            wait_interval = wait_interval * wait_factor
        attempt-=1
    if fail_callback:
        fail_callback(ret)
    return ret

def download(url,filepath,timeout,kwargs):
    if timeout==False:
        timeout=None
    _kw = copy.deepcopy(kwargs)
    buffer = _kw.pop('buffer')
    with closing(requests.get(url, stream=True,timeout=timeout,**_kw)) as response:
        chunk_size = buffer
        data_count = 0
        with open(filepath,'wb') as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                data_count = data_count + len(data)
            return data_count