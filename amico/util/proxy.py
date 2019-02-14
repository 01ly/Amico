import re

def gen_proxy(proxy,kind='text/html'):
    auth = extract_auth(proxy)
    _proxy = extract_ip_port(proxy)
    proxy = _proxy.strip('\n')
    if kind == 'text/html':
        return f'http://{auth}{proxy}'
    if kind == 'media':
        return {
            'http'  : f'http://{auth}{proxy}',
            'https' : f'https://{auth}{proxy}',
        }

def  is_proxy_valid(proxy):
    return re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b\:\d+',proxy)

def extract_auth(proxy):
    res =  re.findall(r'//(.+)@',proxy)
    if res:
        return res[0]+'@'
    return ''

def extract_ip_port(proxy):
    if isinstance(proxy,dict):
        http_proxy = proxy['http']
        return is_proxy_valid(http_proxy)[0]
    else:
        http_proxy = is_proxy_valid(proxy)
        if http_proxy:
            return http_proxy[0]
        else:
            return proxy
