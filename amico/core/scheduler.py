
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
            self.logger.info(f'Requests Queue Size:{req_queue.qsize()}')
        if not req_queue.empty():
            self.waiting = False
            for _ in range(min(self.req_limits,req_queue.qsize())):
                self.recv_req.append(req_queue.get_nowait())
            self.logger.info(f'Left Requests:{req_queue.qsize()}')
        else:
            self.waiting = True
            if all(i.status in ['RUNNING','CLOSE'] for i in self.spiders):
                print('\n* [Done] No Requests to start the crawling.\n')
                raise StopAsyncIteration
            if any_daemon():
                return

    def export(self):
        _export = []
        while self.recv_req:
            _export.append(self.recv_req.pop(0))
        if not self.waiting:
            self.logger.info(f'Exported {len(_export)} Requests.')
        return _export

    def spiders_monitor(self,spiders):
        self.spiders = spiders
        def not_running():
            return all([i.status in ['STOP','PAUSE'] for i in spiders])
        while not_running():
            continue
        if all(i.status=='CLOSE' for i in spiders):
            self.logger.info('* All spiders closed.')
            raise StopAsyncIteration
        for i in spiders:
            if i.status == 'RESUME':
                i.resume()
            if i.status == 'RESTART':
                i.restart()
            if i.status == 'CLOSE':
                i.close(True)

