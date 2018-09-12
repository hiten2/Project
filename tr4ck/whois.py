# Copyright (C) 2018 Bailey Defino
# <https://hiten2.github.io>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import socket
import sys

sys.path.append(os.path.realpath(__file__))

import conf

__doc__ = """RFC 3912-compliant WHOIS implementation"""

global SERVERS
SERVERS = ["whois.iana.org"]

def whois(domain, server = SERVERS[0], timeout = None):
    """
    return the response to a WHOIS request on a domain
    as a list of configuration files
    """
    data = []
    response = []
    sock = socket.create_connection((server, 43), timeout)

    try:
        sock.sendall(domain + "\r\n")
    except socket.error:
        pass

    while not data or data[-1]:
        try:
            data.append(sock.recv(1024))
        except socket.error:
            pass
    data = ''.join(data)
    
    try:
        sock.close()
    except socket.error:
        pass
    return Response(data)

class Response(list):
    """a basic WHOIS response"""

    def __init__(self, response = ''):
        list.__init__(self)
        
        self.empty_line = "\n\n"

        if "\r\n\r\n" in response:
            self.empty_line = "\r\n\r\n"
        
        for category in response.split(self.empty_line):
            self.append(conf.Conf(autosync = False,
                flavor = conf.ConfFlavor(comment = '%')))
            
            try:
                self[-1].load(category)

                if not self[-1]: # omit empty categories
                    raise ValueError()
            except ValueError:
                del self[-1]

    def __str__(self):
        return self.empty_line.join((str(e) for e in self))
