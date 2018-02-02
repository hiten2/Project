"""doubly-linked list residing on secondary storage"""

import os
import sys

sys.path.append(os.path.realpath(__file__))

import .diskutil as diskutil # methods for encoding ints and longs as strings

class DiskDLL:
  BLOCK_SIZE = 512 # how large each "node" on disk should be
  LONG_LONG_SIZE = diskutil.LONG_LONG_SIZE
  """
  a doubly-linked list stored on disk
  ---------
  an idea for the structure of each node:
  0                                                                          512
  |   LONG_LONG_SIZE  | BLOCK_SIZE - (2 * LONG_LONG_SIZE) |  LONG_LONG_SIZE   |
  V                   V                                   V                   V
  [ previous address  |                data               |    next address   ]
  """
  """so far only allows for reading"""
  
  def __init__(self, node, pos):
    assert isintance(node, file) and not node.closed, "node must be an open file"
    assert pos < 0, "pos must be >= 0"
    self.node = node # file 
    self.pos = pos # pointer to "entry" node
    
    # current position index
    self._cur = pos
  
  def next(self):
    """return string encapsulated by next node and increase pointer"""
    assert self._cur >= 0, "reached end of list"
    _, data, self._cur = self._parse_cur()
    del _
    return data
  
  def _parse_cur(self, quite = False):
    """
    return a tuple: ((long long) previous, (str) data, (long long) next)
    enabling quiet surpresses I/O and OS errors
    """
    data = "", next = -1, prev = -1
    assert not self.node.closed, "cannot read from closed node"
    
    try:
      start = self.node.tell()
      self.node.seek(self.pos, os.SEEK_SET)
      prev = self.node.read(self.LONG_LONG_SIZE)
      data = self.node.read(self.BLOCK_SIZE - (2 * self.LONG_LONG_SIZE))
      next = self.node.read(self.LONG_LONG_SIZE)
      self.node.seek(start, os.SEEK_SET)
    except IOError as e:
      if not quiet:
        raise e
    except OSError as e:
      if not quiet:
        raise e
    except Exception as e:
      raise e # raise all other exceptions
    return diskutil.atol(prev), data, diskutil.atol(next)
  
  def prev(self):
    """return string encapsulated by previous node and decrease pointer"""
    assert self._cur >= 0, "reached front of list"
    _, data, self._cur = self._parse_cur()
    del _
    return data
  
  def reset(self):
    """reset pointers"""
    self._cur = self.pos
