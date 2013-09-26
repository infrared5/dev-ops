'''
  Entry for operations related to cloning jenkins master.
  ---
  Available commands
  ---
    clone: clones default jenkins setup based on provided name and port
'''
#!/usr/bin/env python
import os
import sys

import ci.jenkins.util as util
from ci.jenkins.util import COLOR as Color
from ci.jenkins.clone import MasterClone
from ci.jenkins.storage import Storage

STORAGE = Storage(os.path.expanduser('~/.jenkins-clone/clones'))

# TODO: define clone operation

# TODO: define unclone operation
# clone = MasterClone(STORAGE)
# clone.restore(STORAGE.get_clone(name))
# clone.clean()

# TODO: define ls operation (list previous clones created using -clone)

def run_operation(optype):
  ''' Runs associated operation based on provided type. '''
  if optype == 'clone':
    # TODO: Allow for invoke with requested name, port from cli
    clone = MasterClone(STORAGE)
    clone.clone()
  elif optype == 'unclone':
    name = sys.argv[2]
    clone = MasterClone(STORAGE)
    clone.restore(STORAGE.get_clone(name))
    clone.clean()
  elif optype == 'ls':
    util.prettyprint(Color.WHITE, STORAGE.list())

if __name__ == '__main__':
  run_operation(sys.argv[1].lower())
