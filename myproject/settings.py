
#The project name.
PROJECT_NAME  = 'myproject'

#The absolutely sys path of the project.
PATH = r'D:\CODE\Amico\myproject'

#The max nums of the concurrent running tasks at one time in the project
CONCURRENCY = 300

CRAWLING_REQUESTER_MODULE = 'amico.crawl.requester'

#The custom command module path,i.g."myproject.commands"
#If one of the customised commands overrides the native command,
#the native one will be replaced.
COMMANDS_NEW_MODULE = ''

CO_REQUEST_HEADER = {}

LOG_FORMAT = {
    'DEBUG'     : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'INFO'      : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'WARNING'   : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'ERROR'     : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'CRITICAL'  : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}


SPIDER_SERVER_HOST = '127.0.0.1'
SPIDER_SERVER_PORT = 2232

SPIDER_BACKUP_SETTINGS = 'amico.config.spider_settings'

SPIDER_MODULE = 'spiders'

SPIDER_SERVER_COMMANDS_MODULE = 'amico.subcmd'

SPIDERHUB_REQUESTS_QUEUE = 'amico.datatype.queue.FIFOQueue'

