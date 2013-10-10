import os
import shutil
from nose.tools import *
from nose.tools import with_setup
from ci.teamcity.archiver import Archiver

SRC_DIR = 'fooproject'
PROJECT_DIR = os.path.join('.', 'fixtures/teamcity')
PROJECT_NAME = 'barproject'

SRC_PATH = '%s/%s' % (PROJECT_DIR, SRC_DIR)
DEST_PATH = '%s/%s' % (PROJECT_DIR, PROJECT_NAME)

ARCHIVED_PATH = '%s.zip' % DEST_PATH
ZIP_PATH = os.path.join(ARCHIVED_PATH)

archiver = None

def setup_archiver():
  global archiver
  shutil.copytree(SRC_PATH, DEST_PATH)
  archiver = Archiver(PROJECT_DIR)

def teardown_archiver():
  if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)
  archiver = None

@with_setup(setup_archiver, teardown_archiver)
def test_archiver_creates_zip():
  archiver.archive(PROJECT_NAME)
  assert os.path.exists(ZIP_PATH), 'Expected zip file at %s' % ZIP_PATH

@with_setup(setup_archiver, teardown_archiver)
def test_archiver_removes_source_dir():
  archiver.archive(PROJECT_NAME)
  assert not os.path.exists('%s/%s' % (PROJECT_DIR, PROJECT_NAME)), 'Expected archiver to remove target directory.'
