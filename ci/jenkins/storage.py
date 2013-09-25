import os
import sys
import pickle

class Storage():
  def __init__(self, filepath):
    self.filepath = filepath
    self.cache = []
    self.read()

  def get_clone(self, name):
    for clone in self.cache:
      sys.stdout.write('clone: %r' % clone)
      for key, value in clone.items():
        if key == 'name' and value == name:
          return clone
    return None

  def name_exists(self, value):
    for clone in self.cache:
      for key, value in clone.items():
        if key == 'name' and value == value:
          return True
    return False

  def port_exists(self, value):
    for clone in self.cache:
      for key, value in clone.items():
        if key == 'port' and value == value:
          return True
    return False

  def store(self, clone):
    self.cache.append(clone)
    self.write()

  def unstore(self, name):
    clone = self.get_clone(name)
    if clone is not None:
      self.cache = [item for item in self.cache if item != clone]
      self.write()
    return clone

  def write(self):
    with open(self.filepath, 'w+') as f:
      pickle.dump(self.cache, f)

  def read(self):
    directory = os.path.dirname(self.filepath)
    if not os.path.exists(directory):
      os.makedirs(directory)
    self.cache = pickle.load(open(self.filepath, 'r+')) \
      if os.path.exists(self.filepath) else []

  def list(self):
    listing = []
    for clone in self.cache:
      for key, value in clone.items():
        if key == 'name':
          listing.append(value)
    return '\n'.join(name for name in listing) if len(listing) > 0 else '-- none found --'
