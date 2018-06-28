# Copyright (C) 2018 Bailey Defino
# <http://hiten2.asuscomm.com>

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

__doc__ = """RFC 3912-compliant WHOIS client implementation"""

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
    empty_line = "\n\n"

    if "\r\n\r\n" in data:
        empty_line = "\r\n\r\n"
    
    for category in data.split(empty_line):
        response.append(conf.Conf(autosync = False,
            flavor = conf.ConfFlavor(comment = '%')))
        
        try:
            response[-1].load(category)

            if not response[-1]: # omit empty categories
                raise ValueError()
        except ValueError:
            del response[-1]
    return response
