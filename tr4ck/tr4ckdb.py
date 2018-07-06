import os
import scapy.layers
import socket
import sys
import time

sys.path.append(os.path.realpath(__file__))

import db

def dummy(_class, *args, **kwargs):
    """create a dummy database"""
    if len(args) == 4:
        args = args[:3]
    kwargs["store"] = False
    return _class(*args, **kwargs)

class Tr4ckDB(db.DB):
    """
    database base class for tracking, with optional dummy functionality
    
    uses the _generate_id function to categorize data
    """
    
    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            hash = "sha256", store = True):
        db.DB.__init__(self, directory, hash)
        
        self._store = store

    def _generate_id(self, *args, **kwargs):
        """return the described ID for some data"""
        raise NotImplementedError()

    def _parse_id(self, id):
        """parse an ID string generated via self._generate_id"""
        raise NotImplementedError()
    
    def store(self, data):
        """an intelligent wrapper for self.__setitem__"""
        if self._store:
            self[self._generate_id(data)] = str(data)

class DirectedDB(Tr4ckDB):
    """
    a directed database,
    with IDs formatted as: (source, destination, time)
    """
    
    def __init__(self, *args, **kwargs):
        Tr4ckDB.__init__(self, *args, **kwargs)

    def _generate_id(self, *args, **kwargs):
        tup = self._generate_src_dest(*args, **kwargs)

        if tup == None:
            return
        return tup[0], tup[1], "%.10f" % time.time()

    def _generate_src_dest(self, *args, **kwargs):
        """return (src, dest) or None on error"""
        raise NotImplementedError()

    def _parse_id(self, id):
        src, dest, timestamp = id

        try:
            timestamp = float(timestamp)
        except ValueError:
            raise ValueError("invalid timestamp")
        return src, dest, timestamp

class IPDB(DirectedDB):
    """
    an IP-based database for the IP layer
    
    note that specifying fqdn uses DNS requests to determine
    IP address resolution, and in doing so adds to the network traffic
    """

    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            hash = "sha256", store = True, fqdn = False):
        DirectedDB.__init__(self, directory, db_mode, hash, store)

        self._fqdn = fqdn

    def _generate_src_dest(self, packet):
        if scapy.layers.inet.IP in packet:
            dest = packet[scapy.layers.inet.IP].dst
            src = packet[scapy.layers.inet.IP].src
            
            if self._fqdn:
                return socket.getfqdn(src), socket.getfqdn(dest)
            return src, dest
        return

class OuterLayerDB(DirectedDB):
    """MAC-based database for the outermost layer"""

    def __init__(self, *args, **kwargs):
        DirectedDB.__init__(self, *args, **kwargs)
    
    def _generate_src_dest(self, packet):
        if packet:
            return packet.src, packet.dst
        return
