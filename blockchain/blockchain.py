import hashlib
import os
import sys
import time
import urllib2

sys.path.append(os.path.realpath(__file__))

import httpserver

__doc__ = """a basic proof-of-capacity blockchain"""

def Blockchain_handle_connection(conn, directory = os.getcwd(),
        relative = False):
    """handle a connection (i.e. validate the POSTed transaction string)"""
    request_line = []
    
    while not request_line or not request_line[-1] in ('', '\n'):
        try:
            request_line.append(conn.recv(1))
        except socket.error:
            if conn.gettimeout(): # the socket was unexpectedly closed
                return
    request_line = ''.join(request_line)
    
    try:
        request_type, resource, version = request_line.split(' ', 2)
    except ValueError:
        bad_request(conn)
        return
    request_type = request_type.lower()
    resource = resource.lstrip('/')

    if '?' in resource:
        resource = resource[:resource.find('?')]
    
    if not relative:
        resource = os.path.normpath(resource)
    resource = os.path.join(directory, resource)
    
    if not request_type in ("head", "get"):
        not_implemented(conn)
        return
    
    if request_type == "get":
        serve_get(conn, resource)
    elif request_type == "head":
        serve_head(conn, resource)
    close(conn)

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
        httpserver.handle_connection = Blockchain_handle_connection
        httpserver.mainloop()

    def validate(self, trans):################
        """cross-validate a transaction"""
        best = None
        frequencies = {} # nonce: frequency

        for url in self.urls:
            try:
                nonce = Transaction().load(urllib2.urlopen(
                    urllib2.Request(url, str(trans))).read()).nonce
            except: # skip
                continue

            if not frequencies.has_key(nonce):
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
