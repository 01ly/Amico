
import logging


class Logger(object):
    def __init__(self,name):
        self.name = name
        self.logger = logging.getLogger(name)



def getLogger(name):
    logger = Logger(name)
    return logger.logger

def install_root_logger(settings):
    pass

__all__ = ['getLogger']