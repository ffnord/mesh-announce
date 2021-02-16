import json
import os
from psutil import AccessDenied
from psutil import NoSuchProcess
from psutil import process_iter
from psutil import ZombieProcess


def check_process_running(name):
    """ Check if name is a running process.

        The parameter name is case insensitive and does not need do be the whole name, but can be a part of it.
        Returns True in case there was at least one process, whose name contains 'name'.
        Careful: In case of some common errors False is returned without warning.
    """
    for proc in process_iter():
        try:
            if name.lower() in proc.name().lower():
                return True
        except (AccessDenied, NoSuchProcess, ZombieProcess):
            pass
    return False


def _file_name_filter(fname):
    return not (fname.startswith('__') or fname.startswith('.'))

def source_dirs(dir):
    dirs = next(os.walk(dir))[1]
    return filter(_file_name_filter, dirs)

def modules(dir):
    return [os.path.splitext(f)[0] for f in next(os.walk(dir))[2]
        if f.endswith('.py') and _file_name_filter(f)]

def find_modules(base, *path):
    path_files = []
    dir_abs = base
    dir_abs = os.path.join(base, *path)
    dirs = source_dirs(dir_abs)
    for dir in dirs:
        # Ugly hack because python < 3.5 does not support arguments after asterisk expression
        path_files += find_modules(base, *(list(path) + [dir]))

    files = list(modules(dir_abs))
    if len(files) > 0:
        lpath = list(map(os.path.basename, path))
        path_files.append((lpath, files))
    return path_files

def ifindex_to_iface(if_index):
    ifaces = next(os.walk('/sys/class/net'))[1]
    for iface in ifaces:
        index = open('/sys/class/net/' + iface + '/ifindex').read()
        if int(index) == if_index:
            return iface
    return None

def iface_match_recursive(iface, candidates):
    """Check if iface has any connection with an interface from candidates
       through master/slave relationship and return the name of the first
       interface found to have a master/slave relation with it or None if
       there is no relation with any of the interfaces
    """
    # Search up the interface tree, check master of iface
    if os.path.exists('/sys/class/net/' + iface + '/master'):
        master = os.path.basename(os.readlink('/sys/class/net/' + iface + '/master'))
        res = iface_match_recursive(master, candidates)
        if res != None:
            return res

    # Search down the interface tree
    for ciface in candidates:
        # Check current interface
        if ciface == iface:
            return iface
        # Check master of every candidate interface
        if os.path.exists('/sys/class/net/' + ciface + '/master'):
            master = os.path.basename(os.readlink('/sys/class/net/' + ciface + '/master'))
            res = iface_match_recursive(iface, [ master ])
            if res != None:
                return ciface

    return None

def ifindex_to_batiface(if_index, batman_ifaces):
    """Check if the interace with interface index if_index is connected to a
       batman interface in batman_ifaces and return the name of the batman
       interface it is connected with or None if it is not connected to any
       of the specified interfaces
    """
    iface = ifindex_to_iface(if_index)
    if iface in batman_ifaces or iface == None:
        return iface
    return iface_match_recursive(iface, batman_ifaces)
