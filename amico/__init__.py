
__all__ = ['Spider','Request','SpiderHub','Response','Url']

from amico.spider import Spider
from amico.request import Request
from amico.response import Response
from amico.core.spiderhub import SpiderHub
from amico.BaseClass import Url

import sys
if sys.version_info < (3, 5):
    print("Amico requires Python 3.5.x or later version. " )
    sys.exit(1)
del sys