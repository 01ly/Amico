
import re,string
from amico.BaseClass import Command
from amico.exceptions import CommandUsageError
from amico.core.workstation import WorkStation

class AnyNameYouWant(Command):

    requires_project = True

    def handle(self, settings, opts, args):
        if not all(args):
            raise CommandUsageError(self,self.parser)
        spider_names = [re.sub('[%s ]'%string.punctuation,'',i) for i in args]
        works = WorkStation(settings)
        works.work(spider_names=spider_names)

    @classmethod
    def short_desc(self):
        return 'run a specified spider by a given name.'

    def help(self):
        pass

    def syntax(self):
        return ' <spider name> [options] args '
