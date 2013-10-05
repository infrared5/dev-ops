from nose.tools import *
from nose.tools import with_setup
from ci.jenkins.task import TASKS
from ci.jenkins.task import create

TYPEID = TASKS.FILECOPY
PATH = '/home/somewhere'
task = None

def setup_task():
  global task
  task = create({'typeid':TYPEID, 'path':PATH})

def teardown_task():
  global task
  task = None

@with_setup(setup_task, teardown_task)
def test_task_create():
  assert task is not None, 'Expected task to be created.'

@with_setup(setup_task, teardown_task)
def test_task_properties():
  assert task.typeid == TASKS.FILECOPY, 'Expected typid of %d' % TASKS.FILECOPY
  assert task.path == PATH, 'Expected path of %s, was %s' % (PATH, task.path)
