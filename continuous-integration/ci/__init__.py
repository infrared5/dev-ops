import sys

def enum(**enums):
  return type('Enum', (), enums)

def prettyprint(color, message, write=False):
  formatted_msg = '%s%s\033[0m' % (color, message)
  if write:
    sys.stdout.write(formatted_msg)
  else:
    print formatted_msg

COLOR = enum(GREEN='\033[92m', WHITE='\033[97m', YELLOW='\033[93m', BLUE='\033[96m', RED='\033[91m')
