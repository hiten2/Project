import hashlib
import os
import sys
import time
import urllib2

sys.path.append(os.path.realpath(__file__))

import withfile

__doc__ = """a basic proof-of-work blockchain"""

def _int_as_str(i):
    h = hex(i)[2:].rstrip('L')

    if len(h) % 2:
        h = '0' + h
    return h.decode("hex")

def _str_as_int(s):
    return int(s.encode("hex"), 16)

class Blockchain:
    """
    the actual database containing transactions

    this also handles transaction/PoW retrieval
    """
    #########rethink how a transaction enters the distributed blockchain
    ########transaction ID = hash(str(transaction))
    
    def __init__(self, directory = os.getcwd(), urls = (),
            hash = lambda s: hashlib.sha256(s).hexdigest(),
            max_hash = 64 * 'f'):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory
        self.hash = hash
        self.max_hash = max_hash
        self.urls = urls

x    def add(self, trans):
        """add a transaction to the blockchain"""
        trans.prove_work(self.hash, self.max_hash)
        trans.store(self._generate_path(trans))

    def _generate_path(self, trans):
        return os.path.join(self.directory, str(trans.timestamp))

    def get(self, timestamp):
        """get a transaction from the blockchain"""
        trans = Transaction()

        with open(os.path.join(self.directory, str(timestamp)), "rb") as fp:
            with withfile.FileLock(fp):
                trans.load(fp.read())
        return trans

    def validate(self, trans):################
        """cross-validate a transaction"""
        pass

class Transaction:
    """
    a transaction represented as:
        counter + LF + timestamp + LF + data
    """
    
    def __init__(self, data = '', counter = 0, timestamp = None):
        self.data = data
        self.counter = 0

        if not timestamp:
            timestamp = time.time()
        self.timestamp = timestamp

    def load(self, string):
        """load a transaction string into the current instance"""
        self.counter, string = string.split('\n', 1)
        self.counter = int(self.counter)
        self.timestamp, self.data = string.split('\n', 1)
        self.timestamp = float(self.timestamp)

    def prove_work(self, hash, max_hash):
        """
        increment the counter until hash(data + counter) <= max_hash

        the algorithm is as follows:
            1. interpret the data as a base-256 integer
            2. increment the integer and the counter until the integer's
                hash is acceptable
        """
        n = _str_as_int('\n'.join((str(self.timestamp), self.data)))
        
        while hash(_int_as_str(n)) > max_hash:
            self.counter += 1
            n += 1 # minimal speed boost

    def store(self, path):
        """store the transaction to a path"""
        with open(path, "wb") as fp:
            with withfile.FileLock(fp):
                fp.write(str(self))
                os.fdatasync(fp.fileno()) # force data to disk before unlocking

    def __str__(self):
        return "%u\n%f\n%s" % (self.counter, self.timestamp, self.data)

if __name__ == "__main__":
    nzeros = 6
    b = Blockchain("test", max_hash = nzeros * '0' + (64 - nzeros) * 'f')
    t = Transaction("bailey->owen")
    b.add(t)
    print b.get(t)
