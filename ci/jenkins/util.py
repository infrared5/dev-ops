import os
import re
import sys
import shutil
import socket
from ci import enum
from .. import prettyprint, COLOR

PORT_RE = re.compile('(\d{4,5})')

def copyfile(src, dest):
  shutil.copyfile(src, dest)

def copydir(src, dest):
  shutil.copytree(src, dest)

def removefile(path):
  os.remove(path)

def removedir(path):
  shutil.rmtree(path)

def filename_available(value):
  return False if os.path.isfile(value) else True

def port_value_valid(value):
  str_value = value if isinstance(value, str) else str(value)
  return PORT_RE.match(str_value) and value >= 1024 and value <= 65535

def port_available(port):
  available = False
  try:
    prettyprint(COLOR.WHITE, 'Checking for available port on 127.0.0.1:%d ...' % port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', port))
    sock.close()
  except socket.error:
    available = True
  return available
