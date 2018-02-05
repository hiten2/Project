"""long stuff"""

import sys

global LONG_SIZE # Python longs have infinite precision, so this is a generalization
LONG_SIZE = sys.maxint + 1

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
  
  def ltoa(l):
    """return a string representation for a long long"""
    a = ""
    bytes = []
    
    while l > 0:
      bytes.insert(0, 0)
      
      for i in range(8):
        bytes[0] += (l % 2) * (2 ** i)
        l /= 2
    a = "".join((chr(b) for b in bytes))
    return a
