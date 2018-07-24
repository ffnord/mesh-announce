#!/usr/bin/env python3

import json
import argparse

from providers import Provider

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', action='store',
                    help='structure directory', required=True)

parser.add_argument('-b', '--batman', action='store',
                    help='batman-adv device', default='bat0')

args = parser.parse_args()

provider = Provider.from_directory('providers',
    args.directory)

print(json.dumps(provider.call(
        {'batadv_dev': args.batman}
    )
))
