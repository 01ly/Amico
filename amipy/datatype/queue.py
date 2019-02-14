#coding:utf-8
from asyncio import PriorityQueue,Queue,LifoQueue

class FIFO(Queue):

    def __init__(self,maxsize=0):
        super(FIFO, self).__init__(maxsize)

class LIFO(LifoQueue):

    def __init__(self,maxsize=0):
        super(LIFO, self).__init__(maxsize)

class Priority(PriorityQueue):

    def __init__(self,maxsize=0):
        super(PriorityQueue, self).__init__(maxsize)


