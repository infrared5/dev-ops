#!/usr/bin/python
import os
import sys
import argparse
from ci import prettyprint, COLOR as Color
from ci.teamcity.archiver import Archiver

TEAMCITY_DIR = os.path.expanduser('~/.BuildServer')
PROJECT_DIR = os.path.join(TEAMCITY_DIR, 'config/projects')

class Unpack(object):
  pass

parser = argparse.ArgumentParser(description="Utilities for archiving/unarchiving TeamCity projects.")
parser.add_argument('operation', choices=['archive', 'unarchive', 'ls'], \
  help='Define an operation.')
parser.add_argument('-n', '--name', default='', type=str, \
  help='Provide the name of the Project.')

def format_archive_list(listing):
  return '\n'.join(name for name in listing) if len(listing) > 0 else '-- none found --'

def run_operation(operation, name):
  archiver = Archiver(PROJECT_DIR)
  if operation == 'archive':
    try:
      archiver.archive(name)
    except:
      prettyprint(Color.RED, 'Could not archive %s from %s.' % (name, PROJECT_DIR))
  elif operation == 'unarchive':
    try:
      archiver.unarchive(os.path.join(PROJECT_DIR, name), os.path.join(PROJECT_DIR, '%s.zip' % name))
    except:
      prettyprint(Color.RED, 'Could not unarchive %s from %s.' % (name, PROJECT_DIR))
  elif operation == 'ls':
    try:
      prettyprint(Color.WHITE, format_archive_list(archiver.listing()))
    except:
      prettyprint(Color.RED, 'Could not list archives from %s.' % PROJECT_DIR)


if __name__ == '__main__':
  unpack = Unpack()
  args = parser.parse_args(namespace=unpack)
  run_operation(args.operation, args.name)