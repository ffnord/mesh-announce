import os
import subprocess
import traceback
from importlib import import_module

def _set_value(node,path,value):
  ''' Sets a value inside a complex data dictionary.
      The path Array must have at least one element.
  '''
  key = path[0]
  if len(path) == 1:
    node[key] = value;
  elif key in node:
    _set_value(node[key],path[1:],value)
  else:
    node[path[0]] = {}
    _set_value(node[key],path[1:],value)

def _eval_snippet(f, env):
  # definitions of functions used in the snippets go here
  def call(cmdnargs):
    output = subprocess.check_output(cmdnargs)
    lines = output.splitlines()
    lines = [line.decode("utf-8") for line in lines]
    return lines

  real_env = dict(env)
  real_env.update({
    'call': call,
    'socket': import_module('socket'),
  })

  # compile file
  with open(f) as fh:
    code = compile(fh.read(), os.path.abspath(f), 'eval')

  # ensure that files are opened as UTF-8
  import locale
  encoding_backup = locale.getpreferredencoding
  locale.getpreferredencoding = lambda _=None: 'UTF-8'
  try:
    ret = eval(code, real_env)
  finally:
    locale.getpreferredencoding = encoding_backup
  return ret

def gather_data(directory, env = {}):
  data = {}

  if not os.path.isdir(directory):
    return

  for dirname, dirnames, filenames in os.walk(directory):
    for filename in filenames:
      if filename[0] != '.':
        path = os.path.join(dirname, filename)
        relPath = os.path.relpath(path, directory)
        try:
          value = _eval_snippet(path, env)
          _set_value(data, relPath.rsplit(os.sep), value)
        except:
          # print but don't abort
          traceback.print_exc()

  return data
