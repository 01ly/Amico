
from amico.log import getLogger

class Scheduler(object):

    def __init__(self,settings):
        self.req_limits = settings.gets('CONCURRENCY')
        self.recv_req = []
        self.logger = getLogger(__name__)
        self.logger.debug('Loaded scheduler.')


    def receive(self,req_queue):
        self.logger.info(f'Requests Queue Size:{req_queue.qsize()}')
        if not req_queue.empty():
            for _ in range(min(self.req_limits,req_queue.qsize())):
                self.recv_req.append(req_queue.get_nowait())
            self.logger.info(f'Left Requests:{req_queue.qsize()}')
        else:
            print('\n* [Done] No Requests to start the crawling.\n')
            raise StopAsyncIteration


    def export(self):
        _export = []
        while self.recv_req:
            _export.append(self.recv_req.pop(0))
        self.logger.info(f'Exported {len(_export)} Requests.')
        return _export