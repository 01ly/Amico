
from amico.BaseClass import SpiderClientCommand

class SCommand(SpiderClientCommand):


    def parse(self,cmdnae,args,spiders):
        prompt = '''All commands of the Spider-Client:
        \r\n* Usage:
        \r\n  <command> [spider name]
        \r\n* Available commands:
        \r\n       show spiders         show all running spiders and their conditions.
        \r\n       list                 list a general situation of all spiders.
        \r\n       echo                 echo a running spider and its attributes.
        \r\n       pause                pause a running spider by a give name.
        \r\n       stop                 stop a running/paused spider by a give name.
        \r\n       close                close a spider by a give name.
        \r\n       restart              restart a stopped spider by a give name.
        \r\n       resume               resume a paused spider by a give name.
        \r\n       quit                 quit the Spider-Client.
        \r\n       help                 show all the available commands usage.
        '''
        return prompt


