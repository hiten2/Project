import BaseHTTPServer
import hashlib
import os
import SimpleHTTPServer
import sys
import time
import urllib2

__doc__ = """a basic proof-of-work blockchain"""

global BLOCKCHAIN_SINGLETON
BLOCKCHAIN_SINGLETON = None

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

    this also handles counter validation via an HTTP server
    """
    
    def __init__(self, directory = os.getcwd(), urls = (),
            hash = lambda s: hashlib.sha256(s).hexdigest(),
            max_hash = 64 * 'f'):
        global BLOCKCHAIN_SINGLETON
        BLOCKCHAIN_SINGLETON = self
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.directory = directory
        self.hash = hash
        self.max_hash = max_hash
        self.urls = urls

    def add(self, trans):
        """add a transaction to the blockchain (unthreaded)"""
        trans.prove_work(self.hash, self.max_hash)
        trans.store(self._generate_path(trans))

    def _generate_path(self, trans):
        return os.path.join(self.directory, str(trans.timestamp))

    def get(self, timestamp):
        """get a transaction from the blockchain"""
        trans = Transaction()
        trans.load(str(timestamp))
        return trans

    def serve_forever(self, address = ('', 8000)):############
        """start an HTTP server which logs and verifies transactions"""
        server = BaseHTTPServer.HTTPServer(address, BlockchainRequestHandler)
        thread.start_new_thread(server.serve_forever, ())
        print "C2 HTTP server started at %s:%u" % address

        try:
            while 1:
                time.sleep(0.001)
        except KeyboardInterrupt:
            server.shutdown()
            server.server_close()

    def validate(self, trans):################
        """cross-validate a transaction"""
        best = None
        frequencies = {} # counter: frequency

        for url in self.urls:
            try:
                counter = Transaction().load(urllib2.urlopen(
                    urllib2.Request(url, str(trans))).read()).counter
            except: # skip
                continue

            if not frequencies.has_key(counter):
                frequencies[counter] = 0
            frequencies[counter] += 1

class BlockchainRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """a wrapper for the SimpleHTTPServer.SimpleHTTPRequestHandler class"""

    def __init__(self, *args, **kwargs):
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, *args,
            **kwargs)

    def do_GET(self):###########
        """
        wrap SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET,
        but extract request data and categorize as needed
        """
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        
        request_body = self.rfile.read(int(self.headers.getheader(
            'content-length', 0)))

    def do_POST(self):###########
        """
        wrap SimpleHTTPServer.SimpleHTTPRequestHandler.do_POST,
        but extract request data and categorize as needed
        """
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        
        request_body = self.rfile.read(int(self.headers.getheader(
            'content-length', 0)))

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
        data = _str_as_int('\n'.join(self.timestamp, self.data))
        
        while hash(_int_as_str(data)) > max_hash:
            data += 1 # minimal speed boost
            self.counter += 1

    def store(self, path):
        """store the transaction to a path"""
        with open(path, "wb") as fp:
            fp.write(str(self))

    def __str__(self):
        return "%u\r\n%f\r\n%s" % (self.counter, self.timestamp, self.data)

if __name__ == "__main__":
    nzeros = 4
    b = Blockchain("test", max_hash = nzeros * '0' + (64 - nzeros) * 'f')
