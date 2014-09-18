#!/usr/bin/env python3

import json
import argparse
import codecs
import os
import socket
import subprocess

# Force encoding to UTF-8
import locale                                  # Ensures that subsequent open()s
locale.getpreferredencoding = lambda _=None: 'UTF-8'  # are UTF-8 encoded.

import sys
#sys.stdin = open('/dev/stdin', 'r')
#sys.stdout = open('/dev/stdout', 'w')
#sys.stderr = open('/dev/stderr', 'w')

# Utility functions for the announce.d files
def toUTF8(line):
  return line.decode("utf-8")

def call(cmdnargs):
  output = subprocess.check_output(cmdnargs)
  lines = output.splitlines()
  lines = [toUTF8(line) for line in lines]
  return lines

# Local used functions
def setValue(node,path,value):
  ''' Sets a value inside a complex data dictionary.
      The path Array must have at least one element.
  '''
  key = path[0]
  if len(path) == 1:
    node[key] = value;
  elif key in node:
    setValue(node[key],path[1:],value)
  else:
    node[path[0]] = {}
    setValue(node[key],path[1:],value)

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', action='store',
                  help='structure directory',required=True)

parser.add_argument('-b', '--batman', action='store',
                  help='batman-adv device',default='bat0')

args = parser.parse_args()

options = vars(args)

directory = options['directory']
batadv_dev = options['batman']

data = {}

for dirname, dirnames, filenames in os.walk(directory):
  for filename in filenames:
    if filename[0] != '.':
      relPath = os.path.relpath(dirname + os.sep + filename,directory);
      fh = open(dirname + os.sep + filename,'r', errors='replace')
      source = fh.read()
      fh.close()
      value = eval(source)
      setValue(data,relPath.rsplit(os.sep),value)
print(json.dumps(data))
