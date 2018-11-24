
#The project name.
PROJECT_NAME  = 'ladyD'

#The absolutely sys path of the project.
PATH = r'D:\CODE\Amico\ladyD\ladyD'

#Where the spider scripts located.
SPIDER_MODULE = 'ladyD.spiders'

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


REQUESTS_SEND_ONCE = 500

SPIDER_SERVER_HOST = '127.0.0.1'
SPIDER_SERVER_PORT = 2232

SPIDER_DEFAULT_SETTINGS = 'amico.config.spider_settings'


SPIDERHUB_REQUESTS_QUEUE = 'amico.datatype.queue.FIFOQueue'

