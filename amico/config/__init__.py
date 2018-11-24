#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-16
'''

from amico.util.load import load_py

class Settings(dict):

    def __init__(self):
        super(Settings,self).__init__()
        self['project'] = type('project_settings',(),{})


    def set_module(self,path,level='project'):
        _module = load_py(path)
        self[level] = _module

    def gets(self,name,level='project'):
        try:
            return getattr(self[level],name)
        except Exception as e:
            import warnings
            warnings.warn('No attribute "%s" in settings "%s" '%(name,self[level]))





