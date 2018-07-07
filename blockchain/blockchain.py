import os
import sys
import time

__doc__ = """a basic proof-of-capacity blockchain"""

def _int_as_str(i):
    h = hex(i)[2:]

    if len(h) % 2:
        h = '0' + h
    return h.decode("hex")

def _str_as_int(s):
    return int(s.encode("hex"), 16)

class Blockchain:
    def __init__(self, directory = os.getcwd(), min_hash = 0):#########
        self.directory = directory

class Transaction:
    def __init__(self, data, nonce = 0, timestamp = None):
        self.data = _str_as_int(data)
        self.nonce = 0

        if not timestamp:
            timestamp = time.time()
        self.timestamp = timestamp

    def prove_capacity(self, hash, min_hash):
        """increment the nonce until hash(data + nonce) < min_hash"""
        hashed = hash(_int_as_str(self.data + self.nonce))

        while hashed > min_hash:
            self.nonce += 1
            hashed = hash(_int_as_str(self.data + self.nonce))

if __name__ == "__main__":
    import hashlib
    t = Transaction('\0')
    hash = lambda s: hashlib.sha256(s).hexdigest()
    offset = 6
    min_hash = '0' * offset + 'f' * (64 - offset)
    print min_hash
    t.prove_capacity(hash, min_hash)
    print t.nonce
