import os
import sys
import shutil
import traceback

class Archiver():
  def __init__(self, base):
    self.base = base

  def zipdir(self, basedir, dest):
    print 'zip to: %s' % basedir
    for root, dirs, files in os.walk(basedir):
      for f in files:
        dest.write(os.path.join(root, f))
    print 'done.'

  def archive(self, name):
    try:
      print 'running zip!'
      shutil.make_archive(os.path.join(self.base, name), format="zip", root_dir=self.base)
      print 'zip run %s' % self.base
    except:
      traceback.print_exc(file=sys.stdout)