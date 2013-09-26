'''
  Entry for operations related to cloning jenkins master.
  ---
  Available commands
  ---
    clone: clones default jenkins setup based on provided name and port
'''
#!/usr/bin/python
import os
import sys
import argparse

import ci.jenkins.util as util
import ci.jenkins.clone as clone
from ci.jenkins.util import COLOR as Color
from ci.jenkins.clone import MasterClone
from ci.jenkins.storage import Storage

STORAGE = Storage(os.path.expanduser('~/.jenkins-clone/clones'))

class Unpack(object):
  pass

parser = argparse.ArgumentParser(description='Utility to clone and unclone Jenkins instance.')
parser.add_argument('operation', choices=['clone', 'unclone', 'ls'], \
  help='Define the operation.')
parser.add_argument('--name', default=clone.DEFAULT_NAME, type=str, \
  help='Define a name when using operation clone or unclone.')
parser.add_argument('--port', default=clone.DEFAULT_PORT, type=int, \
  help='Optional port when using operation unclone.')

def run_operation(operation, name, port):
  ''' Runs associated operation based on provided type. '''
  if operation == 'clone':
    clone = MasterClone(STORAGE, name, port)
    clone.clone()
  elif operation == 'unclone':
    clone = MasterClone(STORAGE)
    clone.restore(STORAGE.get_clone(name))
    clone.clean()
  elif operation == 'ls':
    util.prettyprint(Color.WHITE, STORAGE.list())

if __name__ == '__main__':
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  run_operation(unpack.operation, unpack.name, unpack.port)
