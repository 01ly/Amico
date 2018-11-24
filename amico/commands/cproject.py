#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''

from amico.exceptions import CommandUsageError
from amico.BaseClass import Command
from amico.util.file import copy_files
from optparse import OptionGroup

class AnyNameYouWant(Command):

    requires_project = False

    def add_options(self,parser):
        group = OptionGroup(parser,'Additional options')
        group.add_option("-d","--dir", metavar="DIR",dest='dir',
                         help="specify the project directory.It must be a absolutely path.")
        parser.add_option_group(group)

    @classmethod
    def short_desc(self):
        return 'create a new crawling project.'

    def handle(self,settings,opts,args):
        import os,amico,re
        if opts.dir:
            if os.path.isdir(opts.dir):
                copy_path = opts.dir
            else:
                raise CommandUsageError(self,self.parser)
        else:
            copy_path = os.getcwd()
        try:
            project_name = re.sub('[^a-zA-Z\d]','',args[0])
        except:
            raise CommandUsageError(self,self.parser)
        destination = os.path.join(copy_path,project_name)
        src = os.path.join(amico.__path__[0],'templates.project'.replace('.',os.sep))
        render_vars = {'project_name':project_name,'project_path':destination}
        render_files = {
            'settings.py.tpl':render_vars
        }
        copy_files(src,destination,('*.pyc','*.pyd'),render=render_files)
        print('* Created a project "%s" at "%s".'%(project_name,destination))
        print('Now you can create a spider then edit it to crawl some websites by:\n')
        print('* check inside the project directory,e.g.')
        print('>> cd %s\n'%project_name)
        print('* Create a crawling spider,e.g.')
        print('>> amico cspider myspider \n')
        print('* Open the spider script and edit it then run it,e.g.')
        print('>> amico runspider myspider\n')
        print('Go and try!')

    def syntax(self):
        return '<project name> [options] [args] '
