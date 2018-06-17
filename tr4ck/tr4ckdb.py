import os
import sys

sys.path.append(os.path.realpath(__file__))

import db

class Tr4ckDB(db.DB):
    """
    database for the tr4ck tool
    
    packets are stored in the following format:
    "source MAC->destination MAC"
    """
    
    def __init__(self, *args, **kwargs):
        db.DB.__init__(self, *args, **kwargs)

    def _generate_id(self, packet):
        """return the described ID for a packet"""
        raise NotImplementedError()
    
    def store(self, packet, mode = "wb"):
        """store the packet based on it addresses"""
        return db.DB.store(self, str(packet), self._generate_id(packet),
            mode = mode)

class PacketDB(Tr4ckDB):
    """packet database"""

    def __init__(self, *args, **kwargs):
        Tr4ckDB.__init__(self, *args, **kwargs)

    def _generate_id(self, packet):
        """source->destination (MAC addresses)"""
        return "->".join((packet.src, packet.dst))