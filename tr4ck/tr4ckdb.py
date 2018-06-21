import os
from scapy.layers import inet
import sys

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
        """parse an ID generated via self._generate_id"""
        raise NotImplementedError()
    
    def store(self, data):
        """an intelligent wrapper for self.__setitem__"""
        if self._store:
            self[self._generate_id(data)] = str(data)

class DirectedDB(Tr4ckDB):
    """
    a directed database,
    with IDs formatted as "source -> destination"
    """
    
    def __init__(self, *args, **kwargs):
        Tr4ckDB.__init__(self, *args, **kwargs)

    def _generate_id(self, *args, **kwargs):
        tup = self._generate_src_dest(*args, **kwargs)

        if tup == None:
            return
        return ' '.join((tup[0], "->", tup[1]))

    def _generate_src_dest(self, *args, **kwargs):
        """return (src, dest) or None on error"""
        raise NotImplementedError()

    def _parse_id(self, id):
        return filter((e.strip() for e in id.split("->")))

class EthernetDB(DirectedDB):
    """MAC-based database for the ethernet layer"""

    def __init__(self, *args, **kwargs):
        DirectedDB.__init__(self, *args, **kwargs)
    
    def _generate_src_dest(self, packet):
        if packet:
            return packet.src, packet.dst
        return

class IPDB(DirectedDB):
    """an IP-based database for the IP layer"""

    def __init__(self, *args, **kwargs):
        DirectedDB.__init__(self, *args, **kwargs)

    def _generate_src_dest(self, packet):
        if inet.IP in packet:
            return packet[inet.IP].src, packet[inet.IP].dst
        return

