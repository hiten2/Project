import hashlib
import os
import sys
import time
import urllib2

sys.path.append(os.path.realpath(__file__))

import filelock

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
    #########should this beacon to a central server instead????
    ########should transactions be accessed via ID or timestamp????
    
    def __init__(self, directory = os.getcwd(), urls = (),
            hash = lambda s: hashlib.sha256(s).hexdigest(),
            max_hash = 64 * 'f'):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory
        self.hash = hash
        self.max_hash = max_hash
        self.urls = urls

    def add(self, trans):
        """add a transaction to the blockchain"""
        trans.prove_work(self.hash, self.max_hash)
        trans.store(self._generate_path(trans))

    def _generate_path(self, trans):
        return os.path.join(self.directory, str(trans.timestamp))

    def get(self, timestamp):
        """get a transaction from the blockchain"""
        trans = Transaction()
        trans.load(str(timestamp))
        return trans

    def validate(self, trans):################
        """cross-validate a transaction"""
        pass

class Transaction:
    """
    a transaction represented as:
        counter + CRLF + timestamp + CRLF + data
    """
    
    def __init__(self, data = '', counter = 0, timestamp = None):
        self.data = data
        self.counter = 0

        if not timestamp:
            timestamp = time.time()
        self.timestamp = timestamp

    def load(self, string):
        """load a transaction string into the current instance"""
        self.counter, string = string.split("\r\n", 1)
        self.counter = int(self.counter)
        self.timestamp, self.data = string.split("\r\n", 1)
        self.timestamp = float(self.timestamp)

    def prove_work(self, hash, max_hash):
        """increment the counter until hash(data + counter) <= max_hash"""
        data = _str_as_int('\n'.join((str(self.timestamp), self.data)))
        
        while hash(_int_as_str(data)) > max_hash:
            data += 1 # minimal speed boost
            self.counter += 1

    def store(self, path):
        """store the transaction to a path"""
        with open(path, "wb") as fp:
            with filelock.FileLock(fp): # synchronize writing
                fp.write(str(self))

    def __str__(self):
        return "%u\r\n%f\r\n%s" % (self.counter, self.timestamp, self.data)

if __name__ == "__main__":
    nzeros = 5
    b = Blockchain("test", max_hash = nzeros * '0' + (64 - nzeros) * 'f')
    t = Transaction("bailey->owen")
    b.add(t)
    print b.get(t)
