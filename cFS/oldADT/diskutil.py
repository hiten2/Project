"""disk stuff"""

__package__ = "cfs"

import os

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
