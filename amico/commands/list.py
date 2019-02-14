
from amico.BaseClass import Command
from amico.core.loader import SpiderLoader

class AnyNameYouWant(Command):

    requires_project = True

    def handle(self,settings,opts, args):
        loader = SpiderLoader(settings)
        spiders = loader.load_all_spiders()
        print(f'\n* Active Amico project:{settings["project"].PROJECT_NAME}')
        print(f'* Found Spiders:{len(spiders)}')
        for _,i in enumerate(spiders):
            print('*','-'*50)
            print(f'* {_+1}. Name:{i.name}   Class:{i.__class__.__name__}  '
                  f'Priority:{i.priority}')
            i.close(save=False)

    @classmethod
    def short_desc(self):
        return 'list all the valid spiders inside the project.'

    def help(self):
        pass

    def syntax(self):
        return '<options> [args]'
