import re,os,string
import amipy
from amipy.BaseClass import Command
from amipy.core.loader import SpiderLoader
from amipy.util.file import copy_files
class AnyNameYouWant(Command):

    requires_project = True

    def handle(self,settings,opts, args):
        print(f'\n* Active Amipy project:{settings["project"].PROJECT_NAME}')
        print(f'* Creating a Spider.')
        spiders  = SpiderLoader(settings).load_all_spiders()
        _exists = []
        for i in spiders:
            i.close(save=False)
            _exists.append(i.name)
        name = re.sub('[%s ]'%string.punctuation,'',args[0])
        if name[0] not in string.ascii_letters:
            print(f'* Invalid name "{name}",please choose another name starts with letters only.')
            return
        if name in _exists:
            print(f'* Name "{name}" has already existed.Please choose another name for your Spider.')
            return
        else:
            _base = os.path.join(settings["project"].PATH,
                                 settings['project'].SPIDER_MODULE.replace('.',os.sep))
            destination = os.path.join(_base,name.title())
            src = os.path.join(amipy.__path__[0], 'templates.spider'.replace('.', os.sep))
            render_vars = {'spider_name': name,
                           'spider_path': destination,
                           'SpiderName':name.title()}
            render_files = {
                'settings.py.tpl': render_vars,
                'spider.py.tpl':render_vars
            }
            copy_files(src, destination, ('*.pyc', '*.pyd'), render=render_files)
            print(f'* Created a spider:{name}')
            print(f'* What to do next?')
            print(f'1. Now you can get inside the "spiders" folder.')
            print(f'2. And you will  see there\'s a "{name.title()}" spider folder.')
            print(f'3. Edit the spider.py under the spider folder.')
            print(f'4. Run the Spider.')

    @classmethod
    def short_desc(self):
        return 'create a new crawling spider.'

    def syntax(self):
        return ' <spider name> [options] <args> '
