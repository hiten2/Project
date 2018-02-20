"""compressed longs (base 256) (human-unfriendly)"""

__package__ = "cfs"

import sys

global LONG_SIZE # Python longs have infinite precision, so this is a generalization

def atol(a):
    """return a long long representation for a string"""
    a = [ord(c) for c in a]
    a.reverse()
    l = 0L

    for i, d in enumerate(a):
        l += d * (256 ** i)
    return l

def ltoa(l):
    """return a string representation for a long long"""
    a = []
    
    while l > 0:
        a.append(chr(l % 256))
        l /= 256
    a.reverse()
    return "".join(a)

LONG_SIZE = len(ltoa(sys.maxint + 1))
