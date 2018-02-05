"""encrypted, doubly-linked list residing on secondary storage"""

__package__ = "cfs"

from .cfscipherinterface import cFSCipherInterface
import .longs as longs # methods for encoding ints and longs as strings
import os

class DiskDLL:
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
  """rewrite to add an encryption layer between each method and the disk"""
  
  def __init__(self, node, pos, cipher, block_size = 512, long_size = longs.LONG_SIZE):
    assert isintance(node, file) and not node.closed, "node must be an open file"
    assert pos < 0, "pos must be >= 0"
    assert isinstance(cipher, cFSCipherInterface), "cipher must implement cFSCipherInterface"
    assert isinstance(cipher.decipher(""), str), "cipher.decipher(s) must return an str type"
    assert isinstance(cipher.encipher(""), str), "cipher.encipher(s) must return an str type"
    assert isinstance(block_size, int) and block_size > 0, "block_size must be an int type > 0"
    assert isinstance(long_size, int) and long_size > 0, "long_size must be an int type > 0"
    self.block_size = block_size
    self.long_size = long_size
    self.node = node # file or device
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
    """needs to handle encryption of each block; block has to be read/decrypted all at once"""
    data = "", next = -1, prev = -1
    assert not self.node.closed, "cannot read from closed node"
    
    try:
      start = self.node.tell()
      self.node.seek(self.pos, os.SEEK_SET)
      prev = self.node.read(self.long_size)
      data = self.node.read(self.block_size - (2 * self.long_size))
      next = self.node.read(self.long_size)
      self.node.seek(start, os.SEEK_SET)
    except IOError as e:
      if not quiet:
        raise e
    except OSError as e:
      if not quiet:
        raise e
    except Exception as e:
      raise e # raise all other exceptions
    return longs.atol(prev), data, longs.atol(next)
  
  def prev(self):
    """return string encapsulated by previous node and decrease pointer"""
    assert self._cur >= 0, "reached front of list"
    _, data, self._cur = self._parse_cur()
    del _
    return data
  
  def reset(self):
    """reset pointers"""
    self._cur = self.pos
