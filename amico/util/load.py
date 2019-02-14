#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import six
import inspect
from pkgutil import iter_modules
from importlib import import_module

def load_py(path):
    """
    *   load an object from a python module path like:
        'amico.spider.Spider'
        it will load the Spider Class from spider.py
    *   load a module by given name:
        'amico.spider'
        it will load module amico.spider as return result
    """
    try:
        index = path.rindex('.')
    except ValueError:
        obj = import_module(path)
        return obj
    module, name = path[:index], path[index + 1:]
    mod = import_module(module)
    try:
        obj = getattr(mod, name)
    except AttributeError:
        obj = import_module(path)
    return obj

def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.
    Referenced from Scrapy.
    """
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods

def iter_spider_classes(module):
    """Return an iterator over all spider classes defined in the given module
    that can be instantiated (ie. which have a name)
    """
    from amico import Spider

    for obj in six.itervalues(vars(module)):
        if inspect.isclass(obj) and \
           issubclass(obj, Spider) and \
           obj.__module__ == module.__name__:
           if getattr(obj, 'name'):
               yield obj
           else:
               from amico.exceptions import SpiderNameNotSet
               raise SpiderNameNotSet(f'Spider {obj.__name__}'
                                      f' does not have a name.')
