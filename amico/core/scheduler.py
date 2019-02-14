
from amico.log import getLogger

class Scheduler(object):

    def __init__(self,settings):
        self.req_limits = settings.gets('CONCURRENCY')
        self.recv_req = []
        self.waiting = False
        self.spiders = None
        self.logger = getLogger(__name__)
        self.logger.debug('Loaded scheduler.')

    def receive(self,req_queue):
        def any_daemon():
            return any(i.status in ['PAUSE','STOP'] for i in self.spiders)
        if not self.waiting:
            self.logger.debug(f'Requests Queue Size:{req_queue.qsize()}')
        if not req_queue.empty():
            self.waiting = False
            for _ in range(min(self.req_limits,req_queue.qsize())):
                self.recv_req.append(req_queue.get_nowait())
                req_queue.task_done()
            self.logger.debug(f'Left Requests:{req_queue.qsize()}')
        else:
            self.waiting = True
            if all(i.status in ['RUNNING','CLOSE'] for i in self.spiders):
                if self._gather_retry():
                    self.logger.info(f'Start to retry {len(self.recv_req)}'
                                     f' Error and Exception pages.')
                    return
                print('\n* [Done] No Requests to start the crawling.\n')
                raise StopAsyncIteration
            if any_daemon():
                return

    def export(self):
        _export = []
        while self.recv_req:
            _export.append(self.recv_req.pop(0))
        if not self.waiting:
            self.logger.debug(f'Exported {len(_export)} Requests.')
        return _export

    def spiders_monitor(self,spiders):
        self.spiders = spiders
        def not_running():
            return all([i.status in ['STOP','PAUSE'] for i in spiders])
        while not_running():
            for i in spiders:
                if i.status=='STOP' and not i.stopped:
                    self.logger.debug(f'Stopping spider {i.name}.')
                    for req in i.binding_hub.requests._queue:
                        if req.spider.name == i.name:
                            i.binding_hub.requests._queue.remove(req)
                            self.logger.debug(f'Removing request {req}.')
                    i.stopped = True
            continue
        if all(i.status=='CLOSE' for i in spiders):
            self.logger.info('* All spiders closed.')
            raise StopAsyncIteration
        for i in spiders:
            if i.status == 'RESUME':
                self.logger.debug(f'Resuming spider {i.name}.')
                i.resume()
            if i.status == 'RESTART':
                self.logger.debug(f'Restarting spider {i.name}.')
                i.restart()
            if i.status == 'CLOSE':
                self.logger.debug(f'Closing spider {i.name}.')
                i.close(True)

    def _gather_retry(self):
        for i in self.spiders:
            if any(i._retries):
                while i._retries:
                    _req = i._retries.pop(0)
                    self.recv_req.append(_req)
                self.logger.info(f'Got {len(self.recv_req)} retry Requests of {i.name}.')
        return bool(self.recv_req)




