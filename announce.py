#!/usr/bin/env python3

import json
import argparse

from gather import gather_data

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', action='store',
                    help='structure directory', required=True)

parser.add_argument('-b', '--batman', action='store',
                    help='main batman-adv device', default='bat0')
parser.add_argument('-bi', dest='batman_extra',
                    action='append',
                    help='another batman-adv devices (fetch another information exclude mac and nodeid)')

args = parser.parse_args()

print(json.dumps(gather_data(
    args.directory,
    {
        'batadv_dev': args.batman,
        'batadv_dev_extra': args.batman_extra
    }
)))
