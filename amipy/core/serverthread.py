
import asyncio
import time
from threading import Thread
from amipy.BaseClass import SpiderClientCommand
from amipy.cmd import _iter_specify_classes

class SpiderServer(Thread):

    def __init__(self,settings,spiders):
        super(SpiderServer,self).__init__()
        self.spiders = spiders
        self.settings = settings
        self.loop = asyncio.new_event_loop()
        self.host = settings['project'].SPIDER_SERVER_HOST
        self.port = settings['project'].SPIDER_SERVER_PORT
        self.tool_module = settings['project'].SPIDER_SERVER_COMMANDS_MODULE
        self.setDaemon(True)
        self.prompt = b"""* Spider-Client commands tool:
                    \r\n* use "help" to see all the commands usage."""

    async def _handle_request(self,reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
        writer.write(self.prompt)
        while 1:
            writer.write(b'\r\n$amipy> ')
            client = writer.get_extra_info('peername')
            _c = ':'.join(str(i) for i in client)
            try:
                await writer.drain()
                data = await reader.readline()
                msg = data.decode().strip()
                if msg == 'quit':
                    print(f'*[Server] {time.ctime()} Connection closed at {_c}')
                    writer.close()
                    return
                elif msg:
                    resp = self.parse_opt(msg)
                    print(f'*[Server] {time.ctime()} Received "{msg}" from {_c}.')
                    writer.write(resp.encode('latin-1'))
            except Exception as e:
                print(f'*[Server] {time.ctime()} {e} at {_c}')
                writer.close()
            if not writer.is_closing():
                await writer.drain()
            else:
                writer.close()
                return

    def _pop_cmdname(self,msg):
        args = [i for i in msg.strip().split(' ') if i]
        import string
        for _,v in enumerate(args):
            if v and v[0] not in string.punctuation:
                args.pop(_)
                if  v in ['help','list'] or(args and args[0][0] not in string.punctuation):
                    return  v,args
        return None,None

    def _get_all_cmds(self,module):
        cmds = {}
        for cmd in _iter_specify_classes(module, cmdcls=SpiderClientCommand):
            cmdname = cmd.__module__.split('.')[-1]
            cmds[cmdname] = cmd
        return cmds

    def parse_opt(self,msg):
        cmdname,args = self._pop_cmdname(msg)
        cmds = self._get_all_cmds(self.tool_module)
        if not cmds.get(cmdname):
            return """\r\n* Command Usage:
            \r\n <option> [spider name] 
            \r\n or:  show spiders
            """
        data = cmds[cmdname]().parse(cmdname,args,self.spiders)
        return data

    def serve(self):
        coro = asyncio.start_server(self._handle_request,self.host,self.port,loop=self.loop)
        server = self.loop.run_until_complete(coro)
        addr,port = server.sockets[0].getsockname()
        print(f'* Spider server serving on {addr}:{port}.')
        print('* Press Ctrl+C to stop the crawling.\n')
        try:
            self.loop.run_forever()
        except (KeyboardInterrupt,StopAsyncIteration):
            print('Shutting down spider server.')
        server.close()
        self.loop.run_until_complete(server.wait_closed())
        self.loop.close()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.serve()




