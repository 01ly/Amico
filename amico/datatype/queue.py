#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-17
'''

from queue import Queue,LifoQueue,PriorityQueue


class FIFO(Queue):

    def __init__(self,maxsize=0):
        super(FIFO, self).__init__(maxsize)

class LIFO(LifoQueue):

    def __init__(self,maxsize=0):
        super(LIFO, self).__init__(maxsize)

class Priority(PriorityQueue):

    def __init__(self,maxsize=0):
        super(PriorityQueue, self).__init__(maxsize)


