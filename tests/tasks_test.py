import os
import sys
from nose.tools import *
from nose.tools import with_setup
from ci.jenkins.task import FileCopyTask
from ci.jenkins.task import DirCopyTask, DirCreateTask
from ci.jenkins.task import CreateUserTask

SRC_DIR = os.path.join('.', 'fixtures/default')
DEST_DIR = os.path.join('.', 'fixtures/temp')
SRC_PATH = os.path.join('.', 'fixtures/default/jenkins')
DEST_PATH = os.path.join('.', 'fixtures/temp/jenkins')

task = None

def setup_filecopy():
  global task
  task = FileCopyTask()

def teardown_filecopy():
  global task
  task.undo()
  task = None

def setup_dircreate():
  global task
  task = DirCreateTask()

def teardown_dircreate():
  global task
  task.undo()
  task = None

def setup_dircopy():
  global task
  task = DirCopyTask()

def teardown_dircopy():
  global task
  task.undo()
  task = None

@with_setup(setup_filecopy, teardown_filecopy)
def test_filecopy_execute():
  assert not os.path.exists(DEST_PATH), \
    'Test required path %s to not previously exist.' % DEST_PATH
  task.execute(SRC_PATH, DEST_PATH)
  assert os.path.exists(DEST_PATH), \
    'Expected %s to be generated.' % DEST_PATH

@with_setup(setup_filecopy, teardown_filecopy)
def test_filecopy_undo():
  task.execute(SRC_PATH, DEST_PATH)
  task.undo()
  assert not os.path.exists(DEST_PATH), \
    'Expected generated destination path %s to be non-existant.' % DEST_PATH

@with_setup(setup_dircreate, teardown_dircreate)
def test_dircreate_execute():
  task.execute(DEST_DIR)
  assert os.path.exists(DEST_DIR), \
    'Expected %s to be generated.' % DEST_DIR

@with_setup(setup_dircreate, teardown_dircreate)
def test_dircreate_undo():
  task.execute(DEST_DIR)
  task.undo()
  assert not os.path.exists(DEST_DIR), \
     'Expected generated destination path %s to be non-existant.' % DEST_DIR

@with_setup(setup_dircopy, teardown_dircopy)
def test_dircopy_execute():
  task.execute(SRC_DIR, DEST_DIR)
  assert os.path.exists(DEST_DIR), \
    'Expected %s to be generated.' % DEST_DIR

@with_setup(setup_dircopy, teardown_dircopy)
def test_dircopy_undo():
  task.execute(SRC_DIR, DEST_DIR)
  task.undo()
  assert not os.path.exists(DEST_DIR), \
     'Expected generated destination path %s to be non-existant.' % DEST_DIR
