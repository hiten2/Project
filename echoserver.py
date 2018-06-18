import socket
import sys
import time

__doc__ = """a simple IPv4 TCP echo server"""
###########add mainloop
###########add N-bytes and port specification

def echo(sock):
    """echo data back through the socket"""
    if not sock:
        return

    try:
        sock.settimeout(0.0) # non-blocking
    except socket.error:
        return
    failed = 0

    while failed < 500:
        try:
            chunk = sock.recv(1024)
        except socket.error:
            chunk = ''

        if not chunk:
            failed += 1
            time.sleep(0.001)
        else:
            failed = 0

            try:
                sock.sendall(chunk)
            except socket.error:
                pass
            print chunk

def echo_http(sock):
    """preface echoed content with an HTTP response header"""
    if not sock:
        return

    try:
        sock.sendall("HTTP/1.1 200 OK\r\n\r\n")
    except socket.error:
        return
    echo(sock)

def help():
    """print help info to STDOUT"""
    print "IPv4 echo server\n" \
          "Usage: python echoserver.py [OPTIONS] [ADDRESS]\n" \
          "OPTIONS\n" \
          "\t-h, --help\tprint help\n" \
          "\t--http\tuse HTTP\n" \
          "ADDRESS\n" \
          "\tan optionally colon-separated address\n" \
          "\te.g. [DOMAIN][:PORT]"

if __name__ == "__main__":
    # argument parsing
    
    domains = "localhost"
    port = 80
    use_http = False

    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            help()
            exit()
        elif arg == "--http":
            use_http = True
        else: # parse
            _domains = arg
            _port = None
            
            if ':' in arg:
                _domains, _port = arg.split(':', 1)
            domains = _domains

            if _port:
                try:
                    _port = int(_port)

                    if _port < 0 or _port >= 2 ** 16:
                        raise ValueError()
                    port = _port
                except ValueError:
                    pass
    
    # server
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sock.bind((domains, port))
    sock.listen(1)

    print "Echo server started on %s:%u" % (domains, port)

    try:
        while 1:
            conn, remote = sock.accept()

            if use_http:
                echo_http(conn)
            else:
                echo(conn)
            conn.close()
    except KeyboardInterrupt:
        pass
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
