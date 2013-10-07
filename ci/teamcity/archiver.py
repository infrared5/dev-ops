import os
import sys
import shutil
import zipfile
import traceback

class Archiver():
  def __init__(self, base):
    self.base = base

  def archive(self, name):
    try:
      location = os.path.join(self.base, name)
      shutil.make_archive(location, format="zip", root_dir=location)
      shutil.rmtree(location)
    except:
      traceback.print_exc(file=sys.stdout)
      raise

  def unarchive(self, dest_dir, zippath):
    try:
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
            if word in (os.curdir, os.pardir, ''): continue
            path = os.path.join(path, word)
          zf.extract(member, path)
      os.remove(zippath)
    except:
      traceback.print_exc(file=sys.stdout)
      raise

  def listing(self):
    try:
      filenames = []
      for f in os.listdir(self.base):
        if f.endswith('.zip'):
          filenames.append(os.path.splitext(f)[0])
      return filenames
    except:
      traceback.print_exc(file=sys.stdout)
      raise
