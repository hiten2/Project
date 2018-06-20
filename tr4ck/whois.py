# Bailey Defino 2018
# <http://hiten2.asuscomm.com>

# CLARIFICATIONS:
#   1. "Authorship Information" regards the following:
#      "Bailey Defino," the year, and "<http://hiten2.asuscomm.com>."
#   2. "Illegal Activity" refers to any activity that falls outside
#       of the laws applicable to the end user.
#   3. "Negative Consequences" are defined by the original author;
#       they include, but are not limited to: illegal activity
#       and property damage.
#   4. "Original Author" refers to the author behind the "Bailey Defino"
#       alias.
#   5. "This License" and "License" refer to the following as they appear
#       on a verbatim copy of this code: authorship information
#       and complete sections entitled: "CLARIFICATIONS," "DISCLAIMER,"
#       "DISTRIBUTION CONDITIONS," and "LICENSE."

# DISCLAIMER:
#   THIS CODE IS PROVIDED WITH NO WARRANTY NOR ANY GAURANTEES.
#  THE ORIGINAL AUTHOR IS NOT RESPONSIBLE FOR ANY NEGATIVE CONSEQUENCES
#   RESULTING FROM ANY ACTION PERFORMED ON OR WITH THE FOLLOWING CODE,
#   REGARDLESS OF WHETHER IT IS A VERBATIM COPY.

# DISTRIBUTION CONDITIONS:
#   (1) The distributed code contains this license,
#   (2) AND either "a" OR "b":
#     (a) the distributed code is a verbatim copy,
#     (b) OR the distributed code asserts that the original author was NOT
#         responsible for any modifications in the distributed code.
#   (3) the distributed code comes without a charge: monetary or otherwise.

# LICENSE:
#   This verbatim code is intellectual property, but is also free
#   and open source software.  This code, verbatim or modified, may only
#   be distributed if ALL of the distribution conditions are met.
#   If not distributed, this code may be modified in any way;
#   however, modification of this code and/or license,
#   does NOT void this original license.
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
