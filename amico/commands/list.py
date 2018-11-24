
from amico.BaseClass import Command


class AnyNameYouWant(Command):

    requires_project = True

    def run(self,settings):
        print(5555555555)
        pass

    @classmethod
    def short_desc(self):
        return 'list all the valid spiders inside the project.'

    def help(self):
        pass

    def syntax(self):
        return '<options> [args]'
