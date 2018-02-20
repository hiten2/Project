"""cFS file API"""

__package__ = "cfs"

import os
from .cfsdirectory import cFSDirectory
from .diskcdll import DiskCDLL

global SEEK_CUR
global SEEK_END
global SEEK_SET
SEEK_CUR = os.SEEK_CUR, SEEK_END = os.SEEK_END, SEEK_SET = os.SEEK_SET

class cFSFile:
  """
  acts similarly to a file, although maintains chunk-based encryption
  using the DiskCDLL class
  """
  
  def __init__(self, parent_dir, node, size, start):
    assert isinstance(parent_dir, cFSDirectory), "parent_dir must be a cFSDirectory instance"
    assert isinstance(node, file) and not node.closed, "node must be an open file instance"
    assert (isinstance(start, int) or isinstance(start, long)) and start > -1, "start must be a long or integer > -1"
    self.dll = DiskCDLL() # NEED ARGS
    self.dll.cipher = self.parent_dir.dll.cipher # same cipher
    self.node = node
    self.parent_dir = parent_dir
    self.size = size
    self.start = start
    
    self._cur = 0
  
  def seek(self, offset, whence = SEEK_CUR):
    """fseek abstraction"""
    pass
  
  def tell(self):
    """return position"""
    return _cur
