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
    def __init__(self, directory = os.getcwd(),
            hash = lambda s: hashlib.sha256(s).hexdigest(),
            max_hash = 32 * 'f'):
        self.directory = directory
        self.hash = hash
        self.max_hash = max_hash

    def add(self, trans):
        self.__enter__()
        trans.prove_capacity(self.hash, self.max_hash)
        trans.store(self._generate_path(trans))

    def __enter__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        return self

    def __exit__(self):
        pass

    def _generate_path(self, trans):
        return os.path.join(self.directory, str(trans.timestamp))

    def get(self, timestamp):
        trans = Transaction()
        trans.load(str(timestamp))
        return trans

class Transaction:
    """
    a transaction stored as:
        nonce + CRLF + timestamp + CRLF + data
    """
    
    def __init__(self, data = '', nonce = 0, timestamp = None):
        self.data = data
        self.nonce = 0

        if not timestamp:
            timestamp = time.time()
        self.timestamp = timestamp

    def load(self, path):
        """load a transaction into the current instance"""
        with open(path, "rb") as fp:
            self.nonce = int(fp.readline().strip())
            self.timestamp = float(fp.readline().strip())
            self.data = fp.read()

    def prove_capacity(self, hash, max_hash):
        """increment the nonce until hash(data + nonce) <= max_hash"""
        data = _str_as_int(self.data)

        while hash(_int_as_str(data)) > max_hash:
            data += 1 # slight efficiency boost
            self.nonce += 1

    def store(self, path):
        """store the transaction to a path"""
        with open(path, "wb") as fp:
            fp.write("%u\r\n%f\r\n" % (self.nonce, self.timestamp))
            fp.write(self.data)

if __name__ == "__main__":
    import hashlib
    t = Transaction('\0')
    hash = lambda s: hashlib.sha256(s).hexdigest()
    offset = 2
    max_hash = offset* '0' + (64 - offset) * 'f'
    print max_hash
    t.prove_capacity(hash, max_hash)
    print t.nonce
