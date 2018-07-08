import hashlib
import os
import sys
import time
import urllib.request, urllib.error, urllib.parse

__doc__ = """a basic proof-of-capacity blockchain"""

def _int_as_str(i):
    h = hex(i)[2:]

    if len(h) % 2:
        h = '0' + h
    return h.decode("hex")

def _str_as_int(s):
    return int(s.encode("hex"), 16)

class Blockchain:
    """
    the actual database (directory/server) containing transactions

    this also handles nonce validation via an HTTP server
    """
    
    def __init__(self, directory = os.getcwd(), urls = (),
            hash = lambda s: hashlib.sha256(s).hexdigest(),
            max_hash = 32 * 'f'):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory
        self.hash = hash
        self.max_hash = max_hash
        self.urls = urls

    def add(self, trans):
        """add a transaction to the blockchain (unthreaded)"""
        trans.prove_capacity(self.hash, self.max_hash)
        trans.store(self._generate_path(trans))

    def _generate_path(self, trans):
        return os.path.join(self.directory, str(trans.timestamp))

    def get(self, timestamp):
        """get a transaction from the blockchain"""
        trans = Transaction()
        trans.load(str(timestamp))
        return trans

    def serve_forever(self):############
        """start an HTTP server which logs and verifies transactions"""
        pass

    def validate(self, trans):################
        """cross-validate a transaction"""
        best = None
        frequencies = {} # nonce: frequency

        for url in self.urls:
            try:
                nonce = Transaction().load(urllib.request.urlopen(
                    urllib.request.Request(url, str(trans))).read()).nonce
            except: # skip
                continue

            if nonce not in frequencies:
                frequencies[nonce] = 0
            frequencies[nonce] += 1

class Transaction:
    """
    a transaction represented as:
        nonce + CRLF + timestamp + CRLF + data
    """
    
    def __init__(self, data = '', nonce = 0, timestamp = None):
        self.data = data
        self.nonce = 0

        if not timestamp:
            timestamp = time.time()
        self.timestamp = timestamp

    def load(self, string):
        """load a transaction string into the current instance"""
        self.nonce, string = string.split("\r\n", 1)
        self.nonce = int(self.nonce)
        self.timestamp, self.data = string.split("\r\n", 1)
        self.timestamp = float(self.timestamp)

    def prove_capacity(self, hash, max_hash):
        """increment the nonce until hash(data + nonce) <= max_hash"""
        data = _str_as_int(self.data)

        while hash(_int_as_str(data)) > max_hash:
            data += 1 # minimal speed boost
            self.nonce += 1

    def store(self, path):
        """store the transaction to a path"""
        with open(path, "wb") as fp:
            fp.write(str(self))

    def __str__(self):
        return "%u\r\n%f\r\n%s" % (self.nonce, self.timestamp, self.data)

if __name__ == "__main__":
    pass
