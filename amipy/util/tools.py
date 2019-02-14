import amipy

def send(request_or_list):
    if isinstance(request_or_list,list):
        for request in request_or_list:
            if not isinstance(request, amipy.Request):
                print(f'[TypeError] not a valid Request to send,'
                                f'got "{type(request).__name__}".')
                continue
            spider = request.spider
            if not isinstance(spider.binding_hub, amipy.SpiderHub):
                print('[TypeError] Not a valid binging SpiderHub for Spider %s,got "%s".'
                                % (spider.name, type(spider.binding_hub).__name__))
                continue
            spider.binding_hub.requests.put_nowait(request)
    elif isinstance(request_or_list, amipy.Request):
        spider = request_or_list.spider
        spider.binding_hub.requests.put_nowait(request_or_list)