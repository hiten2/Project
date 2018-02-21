"""bytearray shredding"""

__package__ = "cfs"

import os

def memshred(arr):
    arr[:] = os.urandom(len(arr))
