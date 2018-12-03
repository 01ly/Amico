#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-16
'''
import amico
import traceback
import warnings
from collections import defaultdict
from amico.util.load import walk_modules,iter_spider_classes,load_py
from amico.log import getLogger

class SpiderLoader(object):

    def __init__(self,settings):
        self.settings = settings
        self._spiders = {}
        self.project_path = settings['project'].PROJECT_NAME
        self._found=defaultdict(list)
        self.warn_only = True
        self.logger = getLogger(__name__)

    @property
    def spiders(self):
        return self._spiders.values()

    @spiders.setter
    def spiders(self,spiders):
        if not isinstance(spiders,dict):
            raise TypeError('Not a valid dict list of spiders.')
        for name,cls in spiders.items():
            if not isinstance(name,str):
                raise TypeError('Not a valid spider name type,got "%s".'
                                %type(name).__name__)
            if not issubclass(cls,amico.Spider):
                raise TypeError('Not a valid Spider subclass,got "%s".'
                                %type(cls).__name__)
            if name in self._spiders:
                import warnings
                warnings.warn('Spider "%s" already exists.'%name)
                continue
            self._spiders.update({name:cls})

    def _singleton_spider(self,cls_):
        def _new(cls,*args,**kwargs):
            if not hasattr(cls, '_instance'):
                cls._instance = super(cls_, cls).__new__(cls)
            return cls._instance
        return _new

    def _load_spider_settings(self,path):
        try:
            settings = load_py(path)
        except ImportError as e:
            import warnings
            warnings.warn(
                'No settings module "%s" found,amico will take "%s" instead.'
                %(path,self.settings['project'].SPIDER_BACKUP_SETTINGS))
            settings = load_py(self.settings['project'].SPIDER_BACKUP_SETTINGS)
        return settings

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            spcls.__new__ = self._singleton_spider(spcls)
            self._found[spcls.name].append((module.__name__, spcls.__name__))
            spcls.__path = module.__name__[:module.__name__.rindex('.')]
            spcls.settings = self._load_spider_settings(
                '.'.join([spcls.__path,'settings']))
            self._spiders[spcls.name] = spcls
            self.logger.debug(f'Loaded spider "{spcls.__name__}:{spcls.name}"')

    def load_all_spiders(self):
        try:
            for module in walk_modules(self.project_path):
                self._load_spiders(module)
        except ImportError as e:
            if self.warn_only:
                msg = ("\n{tb}Could not load spiders from module '{modname}'. "
                       "See above traceback for details.".format(
                    modname=self.project_path, tb=traceback.format_exc()))
                warnings.warn(msg, RuntimeWarning)
            else:
                raise
        else:
            return [i() for i in self.spiders]
