
#The project name.
PROJECT_NAME  = '${project_name}'

#The absolutely sys path of the project.
PATH = r'${project_path}'

#The max nums of the concurrent running tasks at one time in the project
CONCURRENCY = 400

#Where the spider scripts located.
SPIDER_MODULE = '${project_name}.spiders'

#The custom command module path,i.g."myproject.commands"
#If one of the customised commands overrides the native command,
#the native one will be replaced.
COMMANDS_NEW_MODULE = ''

CRAWLING_REQUESTER_MODULE = 'amico.crawl.requester'

CO_REQUEST_HEADER = {}

LOG_FORMAT = {
    'DEBUG'     : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'INFO'      : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'WARNING'   : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'ERROR'     : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'CRITICAL'  : '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}

MIDDLEWARE_TO_INSTALL = {
    'request':{
        'amico.middlewares.requestwares.listhandle':1000,
    },
    'response':{
        'amico.middlewares.responsewares.decode':1000,
    }
}

REQUESTS_SEND_ONCE = 500

SPIDER_SERVER_HOST = '127.0.0.1'
SPIDER_SERVER_PORT = 2232


SPIDER_BACKUP_SETTINGS = 'amico.config.spider_settings'

SPIDER_SERVER_COMMANDS_MODULE = 'amico.subcmd'

SPIDERHUB_REQUESTS_QUEUE = 'amico.datatype.queue.FIFOQueue'

