"""disk representation/interpretation for long longs"""

import os

global LONG_LONG_SIZE
LONG_LONG_SIZE = 8

def atol(a, bytes = LONG_LONG_SIZE):
  """return a long long representation for a string"""
  return

def get_file_size(fp):
  if isinstance(fp, file) and not fp.closed:
    try:
      start = fp.tell()
      fp.seek(0, os.SEEK_END)
      size = fp.tell()
      fp.seek(start, os.SEEK_SET)
      return size
  return 0

def ltoa(l, bytes = LONG_LONG_SIZE):
  """return a string representation for a long long"""
  return
