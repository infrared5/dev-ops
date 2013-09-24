'''
  Entry for operations related to cloning jenkins master.
  ---
  Available commands
  ---
    clone: clones default jenkins setup based on provided name and port
'''
#!/usr/bin/python
import sys
from ci.jenkins.clone import MasterCloner

# TODO: define clone operation
# TODO: define unclone operation
# TODO: define ls operation (list previous clones created using -clone)

def run_operation(optype):
  ''' Runs associated operation based on provided type. '''
  if optype == 'clone':
    # TODO: Allow for invoke with requested name, port from cli
    cloner = MasterCloner()
    cloner.clone()

if __name__ == '__main__':
  run_operation(sys.argv[1].lower())
