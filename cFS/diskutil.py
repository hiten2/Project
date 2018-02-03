"""disk representation/interpretation for long longs"""

import os

global LONG_LONG_SIZE
LONG_LONG_SIZE = 8

def atol(a):
  """return a long long representation for a string"""
  l = 0L
  
  # convert to little endian first
  # so conversion can be done in a cleaner iterative fashion
  bytes = []
  
  for c in a:
    bytes.append(bin(ord(c))[2:][::-1])
  i = 0
  
  for byte in range(len(bytes) - 1, -1, -1):
    for bit in bytes[byte]:
      if bit:
        l += ((long) 2) ** bit # ensure long precision
      i += 1
  return l

def get_file_size(fp, quiet = False):
  """return file size, optionally surpress I/O and OS errors"""
  if isinstance(fp, file) and not fp.closed:
    try:
      start = fp.tell()
      fp.seek(0, os.SEEK_END)
      size = fp.tell()
      fp.seek(start, os.SEEK_SET)
      return size
    except IOError as e:
      if not quiet:
        raise e
    except OSError as e:
      if not quiet:
        raise e
    except Exception as e:
      raise e
  return 0

def ltoa(l):
  """return a string representation for a long long"""
  a = ""
  return a
