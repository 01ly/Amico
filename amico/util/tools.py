import amico

def send(request_or_list):
    if isinstance(request_or_list,list):
        for request in request_or_list:
            if not isinstance(request, amico.Request):
                print(f'[TypeError] not a valid Request to send,'
                                f'got "{type(request).__name__}".')
                continue
            spider = request.spider
            if not isinstance(spider.binding_hub, amico.SpiderHub):
                print('[TypeError] Not a valid binging SpiderHub for Spider %s,got "%s".'
                                % (spider.name, type(spider.binding_hub).__name__))
                continue
            _a = spider.binding_hub.accept(request)
            spider.binding_hub._crawler.convert(_a)
    elif isinstance(request_or_list,amico.Request):
        spider = request_or_list.spider
        _a = spider.binding_hub.accept(request_or_list)
        spider.binding_hub._crawler.convert(_a)