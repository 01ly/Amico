#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-17
'''

import asyncio
from inspect import iscoroutine
from amico.log import getLogger

class Looper(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.logger = getLogger(__name__)

    def run_coroutine(self,coroutines):
        if isinstance(coroutines,list):
            tasks = [asyncio.ensure_future(i) for i in coroutines if iscoroutine(i)]
            _coroutine = asyncio.gather(*tasks)
        elif iscoroutine(coroutines):
            _coroutine = coroutines
        else:
            raise TypeError('Not a coroutine or coroutine list to run with,got "%s".'%type(coroutines).__name__)
        try:
            results = self.loop.run_until_complete(_coroutine)
        except Exception as e:
            _coroutine.cancel()
        else:
            return results

    def run_forever(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.stop()

    def run_tasks(self,tasks):
        if tasks is None:
            return
        try:
            self.loop.run_until_complete(asyncio.gather(*tasks))
        except KeyboardInterrupt:
            self.logger.info('Shutting  down Amico.')
            self.stop()
            raise StopAsyncIteration

    def stop(self):
        tasks = asyncio.Task.all_tasks(loop=self.loop)
        group = asyncio.gather(*tasks, return_exceptions=True)
        group.cancel()
        self.loop.stop()
        self.logger.debug(f'Gathered {len(tasks)} Tasks.')
        self.logger.debug(f'Task Group {group} has been canceled')
        self.logger.debug('Stopped looper.')






