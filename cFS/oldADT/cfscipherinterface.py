"""
cFS cipher interface:
all ciphers cFS uses should implement this"""

__package__ = "cfs"

class cFSCipherInterface:
  def __init__(self, key):
    raise NotImplementedError()
  
  def decipher(self, s):
    raise NotImplementedError()
  
  def encipher(self, s):
    raise NotImplementedError()
