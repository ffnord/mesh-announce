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

def toUTF8(line):
  return line.decode("utf-8")

def call(cmdnargs):
  output = subprocess.check_output(cmdnargs)
  lines = output.splitlines()
  lines = [toUTF8(line) for line in lines]
  return lines

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--directory', action='store',
                  help='structure directory',required=True)

args = parser.parse_args()

options = vars(args)

directory = options['directory']

data = {}

for dirname, dirnames, filenames in os.walk(directory):
  for filename in filenames:
    if filename[0] != '.':
      print(dirname + os.sep + filename)
      fh = open(dirname + os.sep + filename,'r', errors='replace')
      source = fh.read()
      fh.close()
      value = eval(source)
      data[filename] = value
print(dirname + os.sep + filename)
print(json.dumps(data))
