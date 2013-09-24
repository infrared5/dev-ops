#!/usr/bin/python
import sys
from ci.jenkins.clone import MasterCloner

# TODO: define clone operation
# TODO: define unclone operation
# TODO: define ls operation (list previous clones created using -clone)

def run_operation(type):
  if type == 'clone':
    # TODO: Allow for invoke with requested name, port from cli
    cloner = MasterCloner()
    cloner.clone()


if __name__ == '__main__':
  run_operation(sys.argv[1].lower())