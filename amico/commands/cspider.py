
from amico.BaseClass import Command


class AnyNameYouWant(Command):

    requires_project = True

    def run(self,settings):
        print(5555555555)
        pass

    @classmethod
    def short_desc(self):
        return 'create a new crawling spider.'

    def help(self):
        pass

    def syntax(self):
        return ' <spider name> [options] <args> '
