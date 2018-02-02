"""doubly-linked list residing on secondary storage"""

import os
import sys

sys.path.append(os.path.realpath(__file__))

import .diskutil as diskutil # methods for encoding ints and longs as strings

class DiskDLL:
  LONG_LONG_SIZE = diskutil.
  
  def __init__(self, pos):
    self.pos = pos # pointer to "entry" node
    
    # position indices
    self._cur = -1L
    self._next = -1L
    self._prev = -1L
  
  def next(self):
    """return string encapsulated by next node and increase pointer"""
    assert not self._next == -1, "reached end of list"
  
  def prev(self):
    """return string encapsulated by previous node and decrease pointer"""
    assert not self._prev == -1, "reached front of list"
  
  def reset(self):
    """reset pointers"""
    self._cur = self.pos
    self._next = -1, self._prev = -1
