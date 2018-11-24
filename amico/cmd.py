#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''
import os
import sys
import six
import signal
import optparse
from inspect import isclass
from amico.config import Settings
from amico.BaseClass import Command
from amico.util.load import load_py,walk_modules

APSMP = 'AMICO_PROJECT_SETTINGS_PATH'

def _iter_specify_classes(module_name, cmdcls=Command):
    for module in walk_modules(module_name):
        for obj in six.itervalues(vars(module)):
            if isclass(obj) and issubclass(obj, cmdcls) and \
                    obj.__module__ == module.__name__ and \
                    not obj == cmdcls:
                yield obj

def _get_commands_from_module(module, inproject):
    cmds = {}
    for cmd in _iter_specify_classes(module):
        if inproject or not cmd.requires_project:
            cmdname = cmd.__module__.split('.')[-1]
            cmds[cmdname] = cmd
    return cmds

def _get_all_commands(settings, inproject):
    cmds = _get_commands_from_module('amico.commands', inproject)
    try:
        cmds_module = settings['project'].COMMANDS_NEW_MODULE
    except:
        pass
    else:
        if cmds_module:
            cmds.update(_get_commands_from_module(cmds_module, inproject))
    return cmds

def _pop_command_name(args):
    for i in enumerate(args[1:]):
        if not i[1].startswith('-'):
            del args[i[0]+1]
            return i[1]

def _init_project(setPath=False):
    cwd = os.getcwd()
    cwd_files = os.listdir(cwd)
    if 'settings.py' in cwd_files:
        cwd_module = cwd.split(os.sep)[-1]
        setting_module = '.'.join([cwd_module, 'settings'])
        try:
            sys.path.append(cwd[:cwd.rindex(os.sep)])
            _m = load_py(setting_module)
            if getattr(_m, 'PROJECT_NAME'):
                os.environ[APSMP] = setting_module
                if cwd not in sys.path and setPath:
                    sys.path.append(cwd)
                return True
        except:
            return False
    return False

def _get_project_settings():
    if APSMP not in os.environ:
        if not _init_project():
            return None
    path = os.environ.get(APSMP)
    _settings = Settings()
    _settings.set_module(path)
    return _settings

def _print_header(settings, inproject):
    if inproject:
        print("Amico - project: %s\n" % (settings['project'].PROJECT_NAME))
    else:
        print("Amico - no active project\n")

def _print_commands(settings, inproject,cmds):
    _print_header(settings, inproject)
    print("Usage:")
    print("  amico <command> [options] [args]\n")
    print("Available commands:")
    for cmdname, cmd in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmd.short_desc()))
    if not inproject:
        print("\n  [ more ]    More commands available when run from project directory")
    print('\nUse "amico <command> -h" to see more info about a command')

def _print_unknown_command(settings, cmdname, inproject):
    _print_header(settings, inproject)
    print("Unknown command: %s\n" % cmdname)
    print('Use "amico" to see available commands')

def in_project():
    try:
        path = os.environ.get(APSMP)
        load_py(path)
        return True
    except:
        return False

def run(args=None,settings=None):
    if args is None:
        args = sys.argv
    if settings is None or not isinstance(settings,Settings):
        settings = _get_project_settings()
    inproject = in_project()
    cmds = _get_all_commands(settings,inproject)
    cmdname = _pop_command_name(args)
    if not cmdname:
        _print_commands(settings, inproject,cmds)
        sys.exit(0)
    elif cmdname not in cmds:
        _print_unknown_command(settings, cmdname, inproject)
        sys.exit(1)
    cmdcls = cmds[cmdname]
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(),
        conflict_handler='resolve')
    cmd =cmdcls(parser,cmdname)
    parser.usage = 'amico %s %s '%(cmdname,cmd.syntax())
    parser.description = cmd.long_desc()
    cmd.add_options(parser)
    opts, argvs = parser.parse_args(args=args[1:])
    _execute(cmd,settings,opts, argvs)

def _execute(cmd,settings,opts, argvs):
    from amico.exceptions import CommandUsageError
    try:
        cmd.handle(settings, opts, argvs)
    except CommandUsageError as e:
        print('Tip:wrong usage of command "%s".Correct usage e.g.\n'%e.cmd.name)
        e.parser.print_help()

