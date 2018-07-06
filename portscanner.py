import os
import Queue
import socket
import sys
import thread
import time

__doc__ = """port scanning"""

def _get_router_address():
    """return the router's IPv4 address via "ip route"'s default entry"""
    output = []
    
    try:
        stdin, stdout = os.popen2("ip route")
        output = stdout.read().split(' ')
    except (IOError, OSError):
        return

    for fp in (stdin, stdout):
        try:
            fp.close()
        except (IOError, OSError):
            pass
    
    if len(output) > 2 and output[0] == "default":
        return output[2]
    return

def _help():
    """print a help message"""
    print "scan specific ports of ADDRESSES\n" \
          "Usage: python portscanner.py [OPTIONS] [ADDRESSES]\n" \
          "OPTIONS\n" \
          "\t-h, --help\tdisplay this text and exit\n" \
          "\t-n, --nbytes=INT\tthe number of bytes to receive\n" \
          "\t\tif a response scan\n" \
          "\t-p, --ports=CSV\tan unquoted, comma-separated list of ports\n" \
          "\t\tand/or hyphen-separated ranges of ports\n" \
          "\t\t(e.g. \"1-10\" specifies ports 1-10)\n" \
          "\t--prompt=STRING\tthe prompt for a response scan\n" \
          "\t-s, --sort\tsort output by address (waits until generated)\n" \
          "\t-t, --timeout=SECONDS\tthe timeout (default: no timeout)\n" \
          "\t--tcpconnect\trun a TCP connect scan (default)\n" \
          "\t--tcpresponse\trun a TCP response scan\n" \
          "\t--udpresponse\trun a UDP response scan\n" \
          "\t-y, --yesonly\tonly print successful entries\n" \
          "ADDRESSES\n" \
          "\ta space-separated list of IP addresses, subdomains,\n" \
          "\tand/or hostnames\n" \
          "\tif omitted, attempt to scan all addresses in the access\n" \
          "\tpoint's subdomain"

def main():
    """run the main program from sys.argv, without catching SIGINT"""
    i = 1
    ips = []
    names = ("connect", "tcp")
    ports = []
    scankwargs = {}
    sort = False
    timeout = None
    yes_only = False

    while i < len(sys.argv): # parse arguments
        arg = sys.argv[i]

        if arg.startswith("--"):
            arg = arg[2:]

            if arg == "help":
                _help()
                sys.exit()
            elif arg.startswith("nbytes"):
                if '=' in arg:
                    try:
                        scankwargs["nbytes"] = int(arg.split('=', 1)[1])
                    except ValueError:
                        pass
                else:
                    if i == len(sys.argv) - 1:
                        print "Argument required."
                        _help()
                        sys.exit()

                    try:
                        scankwargs["nbytes"] = int(sys.argv[i + 1])
                    except ValueError:
                        pass
                    i += 1
            elif arg.startswith("ports"):
                if '=' in arg:
                    ports += _split_port_csv(arg.split('=', 1)[1])
                else:
                    if i == len(sys.argv) - 1:
                        print "Argument required."
                        _help()
                        sys.exit()
                    ports += _split_port_csv(sys.argv[i + 1])
                    i += 1
            elif arg.startswith("prompt"):
                if '=' in arg:
                    scankwargs["prompt"] = arg.split('=', 1)[1]
                else:
                    if i == len(sys.argv) - 1:
                        print "Argument required."
                        _help()
                        sys.exit()
                    scankwargs["prompt"] = sys.argv[i + 1]
                    i += 1
            elif arg == "sort":
                sort = True
            elif arg.startswith("timeout"):
                if '=' in arg:
                    try:
                        timeout = float(arg.split('=', 1)[1])
                    except ValueError:
                        pass
                else:
                    if i == len(sys.argv) - 1:
                        print "Argument required."
                        _help()
                        sys.exit()
                    try:
                        timeout = float(sys.argv[i + 1])
                    except ValueError:
                        pass
            elif arg == "tcpconnect":
                names = ("connect", "tcp")
            elif arg == "tcpresponse":
                names = ("response", "tcp")
            elif arg == "udpresponse":
                names = ("response", "udp")
            elif arg == "yesonly":
                yes_only = True
            else:
                print "Invalid argument."
                _help()
                sys.exit()
        elif arg.startswith('-'):
            arg = arg[1:]

            for c in arg:
                if c == 'h':
                    _help()
                    sys.exit()
                elif c == 'n':
                    if i == len(sys.argv) - 1:
                        print "Argument required."
                        _help()
                        sys.exit()

                    try:
                        scankwargs["nbytes"] = int(sys.argv[i + 1])
                    except ValueError:
                        pass
                    i += 1
                elif c == 'p':
                    if i == len(sys.argv) - 1:
                        print "Argument required."
                        _help()
                        sys.exit()
                    ports += _split_port_csv(sys.argv[i + 1])
                    i += 1
                elif c == 's':
                    sort = True
                elif c == 't':
                    if i == len(sys.argv) - 1:
                        print "Argument required."
                        _help()
                        sys.exit()

                    try:
                        timeout = float(sys.argv[i + 1])
                    except ValueError:
                        pass
                    i += 1
                elif c == 'y':
                    yes_only = True
                else:
                    print "Invalid flag."
                    _help()
                    sys.exit()
        elif arg:
            ips.append(arg)
        i += 1
    
    if not ips: # no addresses, so scan the router prefix subdomain
        ips = _get_router_address()
        ips = ips[:ips.rfind('.')] # strip final number

    if not ports:
        ports = [21, 22, 25, 80, 8080]
    scanner = SubdomainScanner(_scanclassbynames(names), ips, ports, timeout,
        **scankwargs)
    output = scanner.scan() # is a generator by default

    if sort: # make the list pretty
        try:
            output = sorted(list(output), key = lambda t: t[0])
        except KeyboardInterrupt:
            sys.exit()
    header = "Address" # print a header
    
    if not yes_only:
        header = "Success\t" + header

    if "response" in names:
        header += "\tResponse"
    print header
    
    for address, success, data in output:
        if not data:
            data = ''

        try:
            data = data.encode("unicode-escape")
        except ValueError:
            pass
        
        if yes_only:
            if success:
                if "response" in names:
                    print "%s:%u\t%s" % (address, response)
                else:
                    print "%s:%u" % address
        else:
            if success:
                if "response" in names:
                    print "Yes\t%s:%u\t%s" % (address, response)
                else:
                    print "Yes\t%s:%u" % address
            else:
                print "no\t%s:%u" % address

def _scanclassbynames(names):
    """
    return a scan class by a list/tuple of its names
    e.g. _scanclassbynames(("connect", "tcp")) -> TCPConnectScan
    """
    _map = {("connect", "tcp"): TCPConnectScan,
        ("response", "tcp"): TCPResponseScan,
        ("response", "udp"): UDPResponseScan}
    names = tuple(sorted(names))
    
    if not _map.has_key(names):
        raise KeyError("no such scan")
    return _map[names]

def _split_port_csv(csv):
    """
    split an uncommented CSV string of ports
    e.g. _split_port_csv("1,2,3-5") -> [1, 2, 3, 4, 5]
    """
    ports = []
    
    for p in csv.split(','):
        if '-' in p:
            start, stop = p.split('-', 1)

            try:
                ports += range(int(start), int(stop) + 1)
            except ValueError:
                pass
        else:
            try:
                ports.append(int(p))
            except ValueError:
                pass
    return ports

class Scan:
    """
    base class for a scan
    
    scan constructors should be able to take more arguments than necessary
    """
    
    def __init__(self, ip, port, timeout = None, *args, **kwargs):
        self.ip = ip
        self.port = port
        self.timeout = timeout

    def scan(self):
        """
        return a 3-tuple: (address, success, data)
        where address is a 2-tuple: (self.ip, self.port)

        expected to adhere to self.timeout
        """
        raise NotImplementedError()

class TCPConnectScan(Scan):
    def __init__(self, *args, **kwargs):
        Scan.__init__(self, *args, **kwargs)

    def scan(self):
        output = ((self.ip, self.port), False, None)
        sock = None
        
        try:
            sock = socket.create_connection((self.ip, self.port), self.timeout)
        except socket.error:
            return output
        output = ((self.ip, self.port), True, None)
        
        try:
            sock.close()
        except socket.error:
            pass
        return output

class TCPResponseScan(Scan):
    def __init__(self, ip, port, timeout = None, prompt = None, nbytes = 4096,
            *args, **kwargs):
        Scan.__init__(self, ip, port, timeout, *args, **kwargs)

        self.nbytes = nbytes
        self.prompt = prompt

    def scan(self):
        output = ((self.ip, self.port), False, None)
        sock = None
        
        try:
            sock = socket.create_connection((self.ip, self.port), self.timeout)
        except socket.error:
            return output
        
        if self.prompt:
            try:
                sock.sendall(self.prompt)
            except socket.error:
                pass
        
        try:
            output = ((self.ip, self.port), True, sock.recv(self.nbytes))
        except socket.error:
            pass
        
        try:
            sock.close()
        except socket.error:
            pass
        return output

class UDPResponseScan(Scan):
    def __init__(self, ip, port, timeout = None, prompt = None, nbytes = 4096,
            *args, **kwargs):
        Scan.__init__(self, ip, port, timeout, *args, **kwargs)

        self.nbytes = nbytes
        self.prompt = prompt

    def scan(self):
        output = ((self.ip, self.port), False, None)
        sock = None
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
        except socket.error:
            return output
        
        if self.prompt:
            try:
                sock.sendto(self.prompt, (self.ip, self.port))
            except socket.error:
                pass
        start = time.time()
        
        while self.timeout == None or time.time() - start < self.timeout:
            try:
                _data, _remote = sock.recvfrom(self.nbytes)

                if not _remote == (self.ip, self.port):
                    output = ((self.ip, self.port), True, _data)
                    break
            except socket.error:
                pass
        
        try:
            sock.close()
        except socket.error:
            pass
        return output

class Scanner:
    """
    base class for a port scanner
    
    the constructor's ports argument should ideally be a dictionary,
    with port numbers mapped to keyword arguments for the scanclass constructor
    e.g. {port: {key word: argument}}
    """
    
    def __init__(self, scanclass, ips, ports = None, *scanargs, **scankwargs):
        assert (isinstance(ips, int) or isinstance(ips, list)
            or isinstance(ips, long) or isinstance(ips, str)
            or isinstance(ips, tuple)), \
            "ips must be an int, a list, a long, a string, or a tuple"

        if not isinstance(ips, list) and not isinstance(ips, tuple):
            ips = [ips]
        self.ips = ips
        
        if not ports:
            ports = [21, 22, 25, 80, 8080]
        assert (isinstance(ports, dict) or isinstance(ports, list)
            or isinstance(ports, tuple)), \
            "ports must be a dict of dicts, a list, or a tuple"
        self.ports = ports
        
        if not isinstance(ports, dict):
            self.ports = {}

            for port in ports:
                self.ports[port] = {}
        self._scanargs = scanargs
        self._scankwargs = scankwargs
        assert scanclass, "empty scanclass"
        self._scanclass = scanclass
    
    def scan(self):
        """generate output from Scan.scan"""
        for ip in self.ips:
            for port in self.ports.keys():
                _kwargs = self._scankwargs.copy()

                if self.ports[port]:
                    for k in self.ports[port].keys():
                        _kwargs[k] = self.ports[port][k] # allow overriding
                yield self._scanclass(ip, port, *self._scanargs,
                    **_kwargs).scan()

class ThreadedScanner(Scanner):
    """a basic multithreaded port scanner"""
    
    def __init__(self, *args, **kwargs):
        Scanner.__init__(self, *args, **kwargs)
        
        self._queue = Queue.Queue()

    def _handle_scan(self, ip, port):
        """handle a scan (presumably in a new thread)"""
        _kwargs = self._scankwargs.copy()
        
        if self.ports[port]:
            for k in self.ports[port].keys():
                _kwargs[k] = self.ports[port][k] # allow overriding
        self._queue.put(self._scanclass(ip, port, *self._scanargs,
            **_kwargs).scan())
        thread.exit()

    def scan(self):
        """run the multithreaded scan and print output"""
        active_threads = 0
        max_active_threads = 10

        for ip in self.ips:
            for port in self.ports:
                while (active_threads == max_active_threads
                        and self._queue.empty()):
                    time.sleep(0.001)

                while not self._queue.empty():
                    yield self._queue.get()
                    active_threads -= 1
                
                thread.start_new_thread(self._handle_scan, (ip, port))
                active_threads += 1

        while active_threads:
            while not self._queue.empty():
                yield self._queue.get()
                active_threads -= 1

class SubdomainScanner(ThreadedScanner):
    """a multithreaded port scanner designed for subdomains"""
    
    def __init__(self, *args, **kwargs):
        ThreadedScanner.__init__(self, *args, **kwargs)
        
        self.subdomains = self.ips # workaround to allow for subdomain use
        self.ips = self._generate_subdomains() # -> generator

    def _generate_subdomains(self):
        """generate the applicable subdomains"""
        for subdomain in self.subdomains:
            generate = True

            if subdomain:
                if isinstance(subdomain, int) or isinstance(subdomain, long):
                    base256 = []
                    
                    for i in range(4): # subdomain -> IPv4
                        base256.insert(0, subdomain % 256)
                        subdomain /= 256
                    subdomain = '.'.join((str(e) for e in base256))
                subdomain = subdomain.split('.')
                
                for e in subdomain:
                    try:
                        int(e)
                    except ValueError:
                        generate = False
                        break
            else:
                subdomain = [subdomain]
            
            if generate: # iterate through numeric subdomains
                max_n = 256 ** (4 - len(subdomain))
                n = 0
                
                while n < max_n:
                    base256 = []
                    _n = n
                    
                    for i in range(4 - len(subdomain)): # n -> base 256
                        base256.insert(0, _n % 256)
                        _n /= 256
                    yield '.'.join((str(e) for e in subdomain + base256))
                    n += 1
            else:
                try:
                    yield socket.gethostbyname('.'.join(subdomain))
                except socket.error:
                    pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    sys.exit()
