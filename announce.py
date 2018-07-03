#!/usr/bin/env python3

import json
import argparse

from gather import gather_data

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', action='store',
                    help='structure directory', required=True)

parser.add_argument('-b', '--batman', action='append',
                    help='batman-adv device')

args = parser.parse_args()

if not args.batman:
    args.batman = ['bat0']

print(json.dumps(gather_data(
    args.directory,
    {'batadv_ifaces': args.batman}
)))
