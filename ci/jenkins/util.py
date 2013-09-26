import os
import re
import sys
import shutil
import socket
from . import enum

PORT_RE = re.compile('(\d{4,5})')
COLOR = enum(GREEN='\033[92m', WHITE='\033[97m', YELLOW='\033[93m', BLUE='\033[96m', RED='\033[91m')

def prettyprint(color, message, write=False):
  formatted_msg = '%s%s\033[0m' % (color, message)
  if write:
    sys.stdout.write(formatted_msg)
  else:
    print formatted_msg

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
    prettyprint(COLOR.WHITE, 'Checking for available port on 184.106.134.58:%d ...' % port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('184.106.134.58', port))
    if result == 1:
      available = True
    sock.close()
  except socket.error:
    return False
  return available
