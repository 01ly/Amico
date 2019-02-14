#coding:utf-8

from amipy.util.dbhelper import Database

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)

class Model(dict,metaclass=ModelMetaclass):
    '''Data item model'''

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        self._settings = None

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def __init_db__(self):
        self.db = Database(self._settings.DATABASE_SETTINGS)
        self.db.table = self.__table__
        self.db.connect()

    def save(self,format=None):
        fields = []
        _data = {}
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            value = getattr(self, k, None)
            args.append(value)
            _data[v.name] = value
        if _data:
            self.db.save(_data,format)
            for k, v in self.__mappings__.items():
                setattr(self,k,None)

    def export(self,path,kind='EXCEL'):
        pass

class Field(object):
    '''The base field of the ORM data model'''
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)