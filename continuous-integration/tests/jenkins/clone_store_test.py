import os
import sys
from nose.tools import *
from nose.tools import with_setup
from ci.jenkins.storage import Storage

NAME = 'hello'
PORT = 3001
PATH = os.path.expanduser('~/.jenkins-clone/clone')
store = None

def flushwrite(text):
  sys.stdout.write(text + '\n')
  sys.stdout.flush()

def setup_store():
  global store
  store = Storage(PATH)

def setup_store_single_clone():
  global store
  store = Storage(PATH)
  store.store({'name':NAME, 'port':PORT, 'tasks':[]})

def setup_readin_clone():
  global store
  store = Storage(PATH)
  store.store({'name':NAME, 'port':PORT, 'tasks':[]})
  store.read()

def teardown_store():
  global store
  if os.path.exists(PATH):
    os.remove(PATH)
  store = None

@with_setup(setup_store, teardown_store)
def test_empty_store():
  assert len(store.cache) == 0, \
    'Newly created store should have empty cache.'

@with_setup(setup_store_single_clone, teardown_store)
def test_store_with_clone():
  assert len(store.cache) == 1, \
    'Expected addition of single item.'

@with_setup(setup_store_single_clone, teardown_store)
def test_clone_access():
  assert store.get_clone(NAME) is not None, \
    'Expected single item, was None.'

@with_setup(setup_readin_clone, teardown_store)
def test_readin_clone_access():
  assert store.get_clone(NAME) is not None, \
    'Expected single read-in item, was None'

@with_setup(setup_store_single_clone, teardown_store)
def test_unstore():
  store.unstore(NAME)
  assert store.get_clone(NAME) is None
  assert len(store.cache) == 0, \
    'Expected empty store on unstore().'

@with_setup(setup_readin_clone, teardown_store)
def test_readin_unstore():
  store.unstore(NAME)
  assert store.get_clone(NAME) is None
  assert len(store.cache) == 0, \
    'Expected empty store of read-in item on unstore().'

@with_setup(setup_store_single_clone, teardown_store)
def test_list_print():
  assert store.list() == NAME, \
    'Expecting list() to be %s.' % NAME
