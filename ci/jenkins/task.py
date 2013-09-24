import sys
import util
from subprocess import call

from . import enum

Tasks = enum(FILECOPY=1, DIRCOPY=2, FILECREATE=3, DIRCREATE=4, USERCREATE=5, PERMISSION=6)

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
  def __init__(self, typeid):
    self.id = typeid
    self.path = None

  def execute(self, **kwargs):
    raise TaskException('execute() needs to be overridden by Task subclass.')

  def undo(self):
    raise TaskException('undo() needs to be overridden by Task subclass.')

class FileCopyTask(Task):
  def __init__(self):
    Task.__init__(self, Tasks.FILECOPY)

  def execute(self, source, destination):
    try:
      util.copyfile(source, destination)
      self.path = destination
    except:
      raise TaskException('Could not copy file to %s, from source %s. %r' % (destination, source, sys.exc_info()[0]))

  def undo(self):
    if self.path is not None:
      util.removefile(self.path)

class DirCopyTask(Task):
  def __init__(self):
    Task.__init__(self, Tasks.DIRCOPY)

  def execute(self, source, destination):
    try:
      util.copydir(source, destination)
      self.path = destination
    except:
      raise TaskException('Could not copy directory to %s, from source %s. %r' % (destination, source, sys.exc_info()[0]))

  def undo(self):
    if self.path is not None:
      util.removedir(self.path)

class DirCreateTask(Task):
  def __init__(self):
    Task.__init__(self, Tasks.DIRCREATE)

  def execute(self, dirpath):
    try:
      if not os.path.exists(dirpath):
        os.makedirs(dirpath)
      self.path = dirpath
    except:
      raise TaskException('Could not create directory at %s. %r' % (dirpath, sys.exc_info[0]))

  def undo(self):
    if self.path is not None:
      util.removedir(self.path)

class CreateUserTask(Task):
  def __init__(self):
    Task.__init__(self, Task.USERCREATE)

  def execute(self, username):
    try:
      call(['useradd', username])
      self.path = username
    except:
      raise TaskException('Could not create new user %s. %r' % (username, sys.exc_info[0]))

  def undo(self):
    if self.path is not None:
      call(['userdel', '-r', username])


