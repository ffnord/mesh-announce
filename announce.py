#!/usr/bin/env python3

import json
import argparse

from providers import Provider

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', action='store',
                    help='structure directory', required=True)

parser.add_argument('-b', '--batman', action='store',
                    help='batman-adv device', default=None)
parser.add_argument('-ba', '--babel', action='store',
                    help='address to babel socket', default=None)

args = parser.parse_args()

babel = None
if args.babel is not None:
	ip, port = args.babel.rsplit(':', 1)
	babel = (ip.strip('[]'), int(port))


provider = Provider.from_directory('providers',
    args.directory)

print(json.dumps(provider.call({
        'batadv_dev': args.batman,
        'babel_addr': babel
    })
))
