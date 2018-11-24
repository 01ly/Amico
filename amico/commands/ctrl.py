
from amico.BaseClass import Command


class AnyNameYouWant(Command):

    requires_project = False

    def run(self,settings):
        print(5555555555)
        pass

    @classmethod
    def short_desc(self):
        return 'control the running Amico project.'

    def help(self):
        pass

    def syntax(self):
        return ' <options> [args]'
