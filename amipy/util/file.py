#coding:utf-8
import os
import shutil
from amipy.exceptions import PathDoesntExist

def check_path(path,make=False):
    if os.path.exists(path):
        return True
    else:
        if make:
            os.makedirs(path)
            return True
        return False

def copy_files(src,dst,ignore_pattern,make=True,render=None,strips='.tpl'):
    if not check_path(src):
        raise PathDoesntExist
    if not check_path(dst,make):
        raise PathDoesntExist
    src_files = os.listdir(src)
    ignore_fun = shutil.ignore_patterns(*ignore_pattern)
    filter_matches = ignore_fun(src,src_files)
    for file in src_files:
        if file in filter_matches:
            continue
        srcname = os.path.join(src,file)
        dstname = os.path.join(dst,file.rstrip(strips))
        if os.path.isdir(srcname):
            copy_files(srcname,dstname,ignore_pattern)
        else:
            shutil.copy2(srcname,dstname)
            if render:
                if file in render:
                    _var = render[file]
                    render_template(srcname,dstname,_var)

def render_template(src,dst,var,encoding='utf-8'):
    with open(src,'r',encoding=encoding) as f:
        tpl = f.read()
    import string
    s = string.Template(tpl).safe_substitute(var)
    with open(dst,'w',encoding=encoding) as f:
        f.write(s)

def get_file_size(path=None,size=None):
    if not size:
        size = os.path.getsize(path)
    elif not path:
        size = size
    k = 1024
    if k>size:
        return f'{size}b'
    elif k**2 > size:
        return f'{round(size/k)}KB'
    elif k**3 > size:
        return f'{round(size/k**2,2)}MB'
    elif k**4 <size:
        return f'{round(size/k**3,2)}GB'
