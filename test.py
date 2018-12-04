import os
from amico.cmd import run
os.chdir('myproject')
# print(os.getcwd())
run(['amico','runproject','testpider'])
