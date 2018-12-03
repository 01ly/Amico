
#The project name.
PROJECT_NAME  = r'${project_name}'

#The absolutely sys path of the project.
PATH = r'${project_path}'

#The max nums of the concurrent running tasks at one time in the project
CONCURRENCY = 1000

CRAWLING_REQUESTER_MODULE = 'amico.crawl.requester'

#The custom command module path,i.g."myproject.commands"
#If one of the customised commands overrides the native command,
#the native one will be replaced.
COMMANDS_NEW_MODULE = ''

LOG_ENABLE = True
LOG_LEVEL = 'INFO'
LOG_FILE_ENCODING = 'UTF-8'
LOG_FILE_SAVE_PATH = r'${project_path}\log.log'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = {
    'DEBUG'     : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'INFO'      : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'WARNING'   : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'ERROR'     : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
    'CRITICAL'  : '%(asctime)s %(name)s(%(levelname)s) - %(message)s',
}

MIDDLEWARE_COMMON_INSTALL = {
'request':
    {
        'amico.middlewares.requestwares.ListHandle'     : 1000,
        'amico.middlewares.requestwares.Rules'          : 1000,
        'amico.middlewares.requestwares.ServerCtrl'     : 700,
        'amico.middlewares.requestwares.HeadersHandle'  : 890,
        #place your custom common request handling middleware here
        #e.g. <middleware module path>:<priority>
    },
    'response':
    {
        # place your custom common response handling middleware here
        # e.g. <middleware module path>:<priority>
    },
    'both':
    {
        'amico.middlewares.CrawlFilter' : 900,
        # place your custom common middleware(both on request and response) here
        # e.g. <middleware module path>:<priority>
    }
}

PROJECT_REQUESTS_QUEUE = 'amico.datatype.queue.Priority'

SPIDER_SERVER_ENABLE = True
SPIDER_SERVER_HOST = '127.0.0.1'
SPIDER_SERVER_PORT = 2232

SPIDER_BACKUP_SETTINGS = 'amico.config.spider_settings'

SPIDER_MODULE = 'spiders'

SPIDER_SERVER_COMMANDS_MODULE = 'amico.subcmd'


