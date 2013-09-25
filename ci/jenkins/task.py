import os
import sys
from subprocess import call

from . import enum
import ci.jenkins.util as util

TASKS = enum(FILECOPY=1, DIRCOPY=2, FILECREATE=3, \
  DIRCREATE=4, USERCREATE=5, PERMISSION=6)

class TaskException(Exception):
  '''
    Basic Exception from task execution.
  '''
  def __init__(self, message):
    Exception.__init__(self, message)

class Task():
  '''
    Base Task class.
    * Methods should be overridden.
  '''
  def __init__(self, typeid, path=None):
    self.typeid = typeid
    self.path = path

  def execute(self, **kwargs):
    raise TaskException('execute() needs to be overridden by Task subclass.')

  def undo(self):
    raise TaskException('undo() needs to be overridden by Task subclass.')

  def serialize(self):
    return {
      'typeid': self.typeid,
      'path': self.path
    }

class FileCopyTask(Task):
  def __init__(self):
    Task.__init__(self, TASKS.FILECOPY)
    self.created_dir = False

  def execute(self, source, destination):
    try:
      if not os.path.exists(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
        self.created_dir = True
      util.copyfile(source, destination)
      self.path = destination
    except:
      raise TaskException('Could not copy file to %s, from source %s. %r' \
        % (destination, source, sys.exc_info()[0]))

  def undo(self):
    try:
      if self.path is not None:
        directory = os.path.dirname(self.path)
        util.removefile(self.path)
        if self.created_dir and os.path.exists(directory):
          util.removedir(directory)
    except:
      print 'Could not undo FileCopyTask. %r' % sys.exc_info()[0]

class DirCopyTask(Task):
  def __init__(self):
    Task.__init__(self, TASKS.DIRCOPY)

  def execute(self, source, destination):
    try:
      util.copydir(source, destination)
      self.path = destination
    except:
      raise TaskException('Could not copy directory to %s, from source %s. %r' \
        % (destination, source, sys.exc_info()[0]))

  def undo(self):
    try:
      if self.path is not None:
        util.removedir(self.path)
    except:
      print 'Could not undo DirCopyTask. %r' % sys.exc_info()[0]

class DirCreateTask(Task):
  def __init__(self):
    Task.__init__(self, TASKS.DIRCREATE)

  def execute(self, dirpath):
    try:
      if not os.path.exists(dirpath):
        os.makedirs(dirpath)
      self.path = dirpath
    except:
      raise TaskException('Could not create directory at %s. %r' \
        % (dirpath, sys.exc_info[0]))

  def undo(self):
    try:
      if self.path is not None:
        util.removedir(self.path)
    except:
      print 'Could not undo DirCreateTask. %r' % sys.exc_info()[0]

class CreateUserTask(Task):
  def __init__(self):
    Task.__init__(self, TASKS.USERCREATE)

  def execute(self, username):
    try:
      call(['useradd', username])
      self.path = username
    except:
      raise TaskException('Could not create new user %s. %r' \
        % (username, sys.exc_info[0]))

  def undo(self):
    try:
      if self.path is not None:
        call(['userdel', '-r', self.path])
    except:
      print 'Could not undo CreateUserTask. %r' % sys.exc_info()[0]

FACTORY = {
  TASKS.FILECOPY: FileCopyTask,
  TASKS.DIRCOPY: DirCopyTask,
  TASKS.DIRCREATE: DirCreateTask,
  TASKS.USERCREATE: CreateUserTask
}

def create(plain):
  for key, value in plain.items():
    if key == 'typeid' and value in FACTORY:
      task = FACTORY[value]()
      task.path = plain['path']
      return task
  return None
