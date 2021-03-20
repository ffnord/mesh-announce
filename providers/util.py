import subprocess
import re
import os

RE_BATCTL_VERSION = re.compile('([0-9]+)')
BATCTL_VERSION_2019_3 = [2019, 3]

def call(cmdline):
    output = subprocess.check_output(cmdline)
    lines = output.splitlines()
    lines = [line.decode("utf-8") for line in lines]
    return lines

def call_batctl(batadv_dev, args):
    def get_batctl_version():
        line = call(['batctl', '-v'])[0]
        version_match = [ RE_BATCTL_VERSION.search(elem) for elem in line.split('.') ]
        return [ int(match.groups()[0]) if match else None for match in version_match ]

    batctl_version = get_batctl_version()

    meshif = 'meshif'
    if batctl_version < BATCTL_VERSION_2019_3:
        meshif = '-m'

    base_args = ['batctl', meshif, batadv_dev]

    if os.geteuid() > 0:
        base_args.insert(0, 'sudo')

    return call(base_args + args)
