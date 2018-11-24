
from amico.core.workstation import WorkStation
from amico.BaseClass import Command
from optparse import OptionGroup

class AnyNameYouWant(Command):

    requires_project = True

    def handle(self,settings,opts,args):
        excludes = None
        if opts.exclude:
            import re,string
            excludes = re.sub('[%s ]'%string.punctuation,'',opts.exclude).split(',')
        works = WorkStation(settings)
        works.work(excludes=excludes)

    def add_options(self,parser):
        group = OptionGroup(parser, 'Additional options')
        group.add_option("-e", "--exclude", metavar="SPIDER", dest='exclude',
                         help="run all the spiders inside the project exclude the specified spiders.")
        parser.add_option_group(group)

    @classmethod
    def short_desc(self):
        return 'start to run all the spiders inside the project.'

    def help(self):
        pass

    def syntax(self):
        return ' <project name> [options] [args] '
