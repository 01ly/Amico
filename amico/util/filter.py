import hashlib
from bloompy import SCBloomFilter

def _generate_filter(settings):
    error_rate = settings.BLOOMFILTER_ERROR_RATE
    return SCBloomFilter(error_rate,mode=1)

def _to_feature(request):
    url =request.url
    method = request.method
    params = '' if not request.params else request.params
    data = '' if not request.data else request.data
    _str = ''.join([method, url, params, data])
    _feature = _to_md5(_str)
    return _feature

def _to_md5(_str,encoding='utf-8'):
    bytes_like = bytes(_str, encoding=encoding) if \
        isinstance(_str,str) else _str
    b_md5 = hashlib.md5(bytes_like).hexdigest()
    return b_md5