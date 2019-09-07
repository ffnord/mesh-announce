import os

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
    if os.path.exists('/sys/class/net/' + iface + '/master'):
        master = os.path.basename(os.readlink('/sys/class/net/' + iface + '/master'))
        res = iface_match_recursive(master, candidates)
        if res != None:
            return res

    for ciface in candidates:
        if ciface == iface:
            return iface
        if os.path.exists('/sys/class/net/' + ciface + '/master'):
            master = os.path.basename(os.readlink('/sys/class/net/' + ciface + '/master'))
            res = iface_match_recursive(iface, [ master ])
            if res != None:
                return ciface

    return None

def ifindex_to_batiface(if_index, batman_ifaces):
    iface = ifindex_to_iface(if_index)
    if iface in batman_ifaces or iface == None:
        return iface
    return iface_match_recursive(iface, batman_ifaces)
