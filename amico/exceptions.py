#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''

class SpiderNameNotSet(Exception):
    '''Indicates that spider's unique name is not set yet'''

class SpiderAlreadyExists(Exception):
    '''Indicates that the spider already exists'''

class InvalidDirPath(Exception):
    '''Indicates that the path is invalid'''

class PathDoesntExist(Exception):
    '''Means that the path of template files does not exist'''

class NotValidJsonContent(Exception):
    '''Indicates the content to JSON is not a valid format'''

class DropRequest(Exception):
    '''the Request needs to ignore,then drop it'''

class Forbidden(Exception):
    '''Amico forbidden options.'''

class CommandUsageError(Exception):
    '''a command usage error'''
    def __init__(self,cmd,parser):
        self.cmd = cmd
        self.parser = parser

