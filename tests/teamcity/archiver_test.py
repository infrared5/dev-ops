import os
from nose.tools import *
from nose.tools import with_setup
from ci.teamcity.archiver import Archiver

PROJECT_DIR = os.path.join('.', 'fixtures/teamcity')
PROJECT_NAME = 'fooproject'
ZIP_PATH = os.path.join(PROJECT_DIR, '%s.zip' % PROJECT_NAME)
archiver = None

def setup_archiver():
  global archiver
  archiver = Archiver(PROJECT_DIR)

def teardown_archiver():
  # if os.path.exists(ZIP_PATH):
  #   os.remove(ZIP_PATH)
  archiver = None

@with_setup(setup_archiver, teardown_archiver)
def test_archiver_creates_zip():
  archiver.archive(PROJECT_NAME)
  assert os.path.exists(ZIP_PATH), 'Expected zip file at %s' % ZIP_PATH

