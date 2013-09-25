import os
import re
import sys
import fileinput
import traceback
from subprocess import call

import ci.jenkins.util as util
from ci.jenkins.util import COLOR as Color
from ci.jenkins.task import FileCopyTask
from ci.jenkins.task import DirCopyTask, DirCreateTask
from ci.jenkins.task import CreateUserTask
from ci.jenkins.task import create

CONFIG_LOCATION = '/etc/default'
INIT_LOCATION = '/etc/init.d'
RUN_LOCATION = '/var/run'
DEFAULT_NAME = 'jenkins'
DEFAULT_PORT = 8080

# ---
# ADDITIONS
# ---
# /home/$name
# /var/run/$name/jenkins.pid
# /var/lib/$name
# /usr/share/$name
# /etc/init.d/$name
# /etc/default/$name

class MasterClone():

  def __init__(self, storage, name=DEFAULT_NAME, port=DEFAULT_PORT):
    self.storage = storage
    self.name = name
    self.port = port
    self.tasks = []

  def clone(self):
    try:
      if self.name is DEFAULT_NAME:
        self.request_name()
      if self.port is DEFAULT_PORT:
        self.request_port()
      if self.establish():
        self.deploy()
        self.storage.store(self.serialize())
    except KeyboardInterrupt:
      self.clean()

  def serialize(self):
    return {
      'name': self.name,
      'port': self.port,
      'tasks': [task.serialize() for task in self.tasks]
    }

  def restore(self, cache):
    self.name = cache['name']
    self.port = cache['port']
    self.tasks = [create(task) for task in cache['tasks']]
    self.tasks = [task for task in self.tasks if task is not None]

  def clean(self):
    '''
      Empties and undos previously performed tasks.
    '''
    for task in self.tasks[:]:
      task.undo()
      self.tasks.remove(task)
    self.storage.unstore(self.name)

  def ensure_prefix(self, value):
    '''
      Ensures that value has prefix of 'jenkins-' (sans-quotes).
    '''
    return value if value.find(DEFAULT_NAME) == 0 else '%s-%s' % (DEFAULT_NAME, value)

  def request_name(self):
    '''
      Prompt for unique identifier name of new jenkins instance.
    '''
    while True:
      util.prettyprint(Color.BLUE, 'Enter name: ', write=True)
      self.name = raw_input().lower()
      if self.name is not None and self.name is not '':
        self.name = self.ensure_prefix(self.name)
        if self.storage.name_exists(self.name):
          util.prettyprint(Color.YELLOW, '%s is already taken. Please provide another name.\n' % self.name)
        elif util.filename_available('%s/%s' % (INIT_LOCATION, self.name)):
          util.prettyprint(Color.WHITE, 'Accepting provided name: %s' % self.name)
          return True
        else:
          util.prettyprint(Color.YELLOW, '%s is already taken. Please provide another name.\n' % self.name)
      else:
        util.prettyprint(Color.YELLOW, 'Please enter a new name for the jenkins clone.\n')

  def request_port(self):
    '''
      Prompt for specific port to use.
    '''
    while True:
      util.prettyprint(Color.BLUE, 'Enter port to use: ', write=True)
      try:
        self.port = int(raw_input().lower())
        if not util.port_value_valid(self.port):
          util.prettyprint(Color.YELLOW, 'Please enter a 4-digit integer to use for the port.')
        elif self.storage.port_exists(self.port):
          util.prettyprint(Color.YELLOW, '%s is already taken. Please provide another port.' % self.port)
        elif util.port_available(self.port):
          util.prettyprint(Color.WHITE, 'Accepting provided port: %d' % self.port)
          return True
        else:
          util.prettyprint(Color.YELLOW, '%s is already taken. Please provide another port.' % self.port)
      except:
        util.prettyprint(Color.YELLOW, 'Please enter a valid port number for the jenkins clone to run on.')

  def replace_pid_reference(self, line):
    ''' Returns modified line with new pid reference. '''
    pid_location = re.compile('PIDFILE=(.*)').match(line).group()
    return pid_location.replace('/jenkins/', '/%s/' % self.name, 1)

  def replace_war_location(self, line):
    ''' Returns old war and new war locations in tuple. '''
    war_match = re.compile('JENKINS_WAR=(.*)/(.*).war').match(line)
    war_directory = war_match.group(1)
    filename = war_match.group(2)
    war_location = '%s/%s.war' % (war_directory, filename)
    dest_war_directory = war_directory.replace('/jenkins', '/%s' % self.name, 1)
    dest_war_location = '%s/%s.war' % (dest_war_directory, filename)
    return war_location, dest_war_location

  def replace_home_location(self, line):
    ''' Returns old home and new home locations in tuple. '''
    home_location = re.compile('JENKINS_HOME=(.*)').match(line).group(1)
    dest_home_location = home_location.replace('/jenkins', '/%s' % self.name, 1)
    return home_location, dest_home_location

  def establish(self):
    '''
      Attempts to copy and setup new jenkins server.
      Aborts if exceptions raised.
    '''
    try:
      self.copy_init()
      self.copy_config()
      return True
    except:
      util.prettyprint(Color.RED, 'Error in cloning for %s:%d. %r' % (self.name, self.port, sys.exc_info()[0]))
      util.prettyprint(Color.GREEN, traceback.print_exc())
      self.clean()
      return False
    return False

  def copy_init(self):
    '''
      Copies /etc/init.d script to new location.
    '''
    source_init = '%s/%s' % (INIT_LOCATION, DEFAULT_NAME)
    dest_init = '%s/%s' % (INIT_LOCATION, self.name)
    task = FileCopyTask()
    self.tasks.append(task)
    task.execute(source_init, dest_init)
    for line in fileinput.input(os.path.abspath(dest_init), inplace=True):
      if re.search('^NAME=', line) is not None:
        line = 'NAME=%s\n' % self.name
      sys.stdout.write(line)
    call(['chmod', '775', dest_init])

  def copy_config(self):
    '''
      Copies /etc/default configuration to new location.
      Loaded by init.d script.
    '''
    src = '%s/%s' % (CONFIG_LOCATION, DEFAULT_NAME)
    dest = '%s/%s' % (CONFIG_LOCATION, self.name)
    task = FileCopyTask()
    self.tasks.append(task)
    task.execute(src, dest)
    util.prettyprint(Color.WHITE, 'Preparing configuration for %s on port %d.' % (self.name, self.port))
    for line in fileinput.input(os.path.abspath(dest), inplace=True):
      if re.search('^NAME=', line) is not None:
        line = 'NAME=%s' % self.name
      elif re.search('^PIDFILE=', line) is not None:
        line = self.replace_pid_reference(line)
      elif re.search('^JENKINS_WAR=', line) is not None:
        war_location, dest_war_location = self.replace_war_location(line)
        copy_task = FileCopyTask()
        create_dir_task = DirCreateTask()
        self.tasks.extend([create_dir_task, copy_task])
        copy_task.execute(war_location, dest_war_location)
        create_dir_task.execute(os.path.dirname(dest_war_location))
        line = 'JENKINS_WAR=%s' % dest_war_location
      elif re.search('^JENKINS_HOME=', line) is not None:
        home_location, dest_home_location = self.replace_home_location(line)
        copy_dir_task = DirCopyTask()
        self.tasks.append(copy_dir_task)
        copy_dir_task.execute(home_location, dest_home_location)
        line = 'JENKINS_HOME=%s' % dest_home_location
      elif re.search('^HTTP_PORT', line) is not None:
        line = 'HTTP_PORT=%s' % str(self.port)
      sys.stdout.write(line)
    util.prettyprint(Color.WHITE, 'Reassigning ownership on %s...' % dest_home_location)
    adduser = CreateUserTask()
    self.tasks.append(adduser)
    adduser.execute(self.name)
    # Change permissions on newly created home directory
    call(['chown', '-R', 'jenkins:nogroup', dest_home_location])
    util.prettyprint(Color.WHITE, 'Ownership reassigned successfully.')

  def deploy(self):
    '''
      Starts new instance of jenkins as daemon
    '''
    util.prettyprint(Color.WHITE, 'Starting %s...' % self.name)
    try:
      call(['sudo', '%s/%s' % (INIT_LOCATION, self.name), 'start'])
      call(['chown', '-R', 'jenkins:adm', '%s/%s' % (RUN_LOCATION, self.name)])
      task = DirCreateTask()
      task.path = '%s/%s' % (RUN_LOCATION, self.name)
      self.tasks.append(task)
      # TODO: add task for starting server so as to undo()
    except:
      util.prettyprint(Color.RED, 'Unexpected error in starting daemon: %r' % sys.exc_info()[0])
      raise
