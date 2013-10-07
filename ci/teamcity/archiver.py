'''
  Archiving utilities related to TeamCity Build projects.
'''
import os
import sys
import shutil
import zipfile
import traceback

class Archiver():
  '''
    Archiver is responsible for archiving (generating ZIP) and
    unarchiving Build projects under TeamCity.
  '''
  def __init__(self, base):
    self.base = base

  def archive(self, name):
    '''
      Archives directory under provided base location.
    '''
    try:
      location = os.path.join(self.base, name)
      shutil.make_archive(location, format="zip", root_dir=location)
      shutil.rmtree(location)
    except:
      traceback.print_exc(file=sys.stdout)
      raise

  def unarchive(self, zipname):
    '''
      Unarchives zip in destination directory.
    '''
    try:
      zippath = os.path.join(self.base, '%s.zip' % zipname)
      dest_dir = os.path.join(self.base, zipname)
      # Unarchive for 2.7 copied from
      # http://stackoverflow.com/questions/12886768/simple-way-to-unzip-file-in-python-on-all-oses
      with zipfile.ZipFile(zippath) as zf:
        for member in zf.infolist():
          # Path traversal defense copied from
          # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
          words = member.filename.split('/')
          path = dest_dir
          for word in words[:-1]:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir, ''): 
              continue
            path = os.path.join(path, word)
          zf.extract(member, path)
      os.remove(zippath)
    except:
      traceback.print_exc(file=sys.stdout)
      raise

  def listing(self):
    '''
      Returns listing of files with extension '.zip' wihtin base location.
    '''
    try:
      filenames = []
      for f in os.listdir(self.base):
        if f.endswith('.zip'):
          filenames.append(os.path.splitext(f)[0])
      return filenames
    except:
      traceback.print_exc(file=sys.stdout)
      raise
