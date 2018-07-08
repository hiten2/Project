import os
import socket
import sys
import thread

__doc__ = """a simple, functional HTTP server"""

def bad_request(conn):
    error_close(conn, 400, "bad request")

def close(filelike):
    try:
        filelike.close()
    except (IOError, OSError, socket.error):
        pass

def error_close(conn, code, status):
    send_status_line(conn, code, status)
    terminate_header(conn)
    close(conn)

def forbidden(conn):
    error_close(conn, 403, "forbidden")

def handle_connection(conn, directory = os.getcwd(), relative = False):
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

def _help():
    print "a simple, functional HTTP server\n" \
          "Usage: python httpserver.py [OPTIONS] [INTERFACE][:PORT]\n" \
          "OPTIONS\n" \
          "\t-b, --backlog=INT\tthe server backlog\n" \
          "\t-d, --directory=PATH\tthe root directory for resources\n" \
          "\t-h, --help\tprint this help and exit\n" \
          "\t-r, --relative\tallow relative paths\n" \
          "\t-t, --threaded\tthread new connections\n" \
          "INTERFACE\n" \
          "\tthe interface to listen on\n" \
          "\tdefaults to 0.0.0.0\n" \
          "PORT\n" \
          "\tthe port number (an integer in the range 0-65535)\n" \
          "\tdefaults to 80"

def mainloop(directory = os.getcwd(), relative = False, address = ('', 80),
        backlog = 1, threaded = False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(0.1)
    
    sock.bind(address)
    sock.listen(backlog)
    
    try:
        while 1:
            try:
                conn, remote = sock.accept()
            except socket.error:
                continue
            print "%s:%u" % remote

            if threaded:
                thread.start_new_thread(handle_connection, (conn, directory,
                    relative))
            else:
                handle_connection(conn, directory, relative)
    except KeyboardInterrupt:
        pass
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def not_found(conn):
    error_close(conn, 404, "not found")

def not_implemented(conn):
    error_close(conn, 501, "not implemented")

def ok(conn):
    send_status_line(conn, 200, "ok")

def send(conn, data):
    try:
        conn.sendall(data)
    except socket.error:
        pass

def send_header(conn, key, value):
    send(conn, "%s: %s\r\n" % (str(key).title(), str(value)))

def send_status_line(conn, code, status):
    send(conn, "HTTP/1.0 %u %s\r\n" % (int(code), str(status).upper()))

def serve_get(conn, resource):
    fp = serve_head(conn, resource, True)

    if not fp:
        return
    chunk = fp.read(4096)

    while chunk:
        send(conn, chunk)

        try:
            chunk = fp.read(4096)
        except (IOError, OSError):
            pass
    close(fp)

def serve_head(conn, resource, returnfp = False):
    fp = resource # resource could be a path or a file
    opened = not isinstance(fp, file)
    
    if isinstance(resource, str):
        if resource.rstrip('/') == os.getcwd():
            resource = os.path.join(resource, "index.html")

        if not os.path.exists(resource):
            not_found(conn)
            return
        elif not os.access(resource, os.R_OK):
            forbidden(conn)
            return
        
        try:
            fp = open(resource, "rb")
        except (IOError, OSError):
            unknown(conn)
            return
    ok(conn)
    
    try:
        send_header(conn, "content-length", sizeof(fp))
    except (IOError, OSError):
        unknown(conn)
        return
    terminate_header(conn)

    if returnfp:
        return fp
    close(fp)

def sizeof(fp):
    start = fp.tell()
    fp.seek(0, os.SEEK_END)
    size = fp.tell()
    fp.seek(start, os.SEEK_SET)
    return size

def terminate_header(conn):
    send(conn, "\r\n")

def unknown(conn):
    error_close(conn, 520, "unknown error")

if __name__ == "__main__":
    backlog = 1
    directory = os.getcwd()
    i = 1
    interface = ''
    port = 80
    relative = False
    threaded = False

    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg.startswith("--"):
            arg = arg[2:]

            if arg == "backlog":
                if len(sys.argv) == i + 1:
                    print "Required argument."
                    _help()
                    sys.exit()

                try:
                    backlog = int(sys.argv[i + 1])
                except ValueError:
                    print "Invalid backlog."
                    _help()
                    sys.exit()
                i += 1
            elif arg == "directory":
                if len(sys.argv) == i + 1:
                    print "Required argument."
                    _help()
                    sys.exit()
                directory = sys.argv[i + 1]
                i += 1
            elif arg == "help":
                _help()
                sys.exit()
            elif arg == "relative":
                relative = True
            elif arg == "threaded":
                threaded = True
            else:
                print "Invalid argument."
                _help()
                sys.exit()
        elif arg.startswith('-'):
            for c in arg[1:]:
                if c == 'b':
                    if len(sys.argv) == i + 1:
                        print "Required argument."
                        _help()
                        sys.exit()

                    try:
                        backlog = int(sys.argv[i + 1])
                    except ValueError:
                        print "Invalid backlog."
                        _help()
                        sys.exit()
                    i += 1
                elif c == 'd':
                    if len(sys.argv) == i + 1:
                        print "Required argument."
                        _help()
                        sys.exit()
                    directory = sys.argv[i + 1]
                    i += 1
                elif c == 'h':
                    _help()
                    sys.exit()
                elif c == 'r':
                    relative = True
                elif c == 't':
                    threaded = True
                else:
                    print "Invalid option."
                    _help()
                    sys.exit()
        else:
            interface = arg

            if ':' in arg:
                interface, _port = arg.split(':', 1)

                try:
                    port = int(_port)

                    if port < 0 or port > 65535:
                        raise ValueError()
                except ValueError:
                    print "Invalid port."
                    _help()
                    sys.exit()
        i += 1
    mainloop(directory, relative, (interface, port), backlog)
