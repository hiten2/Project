import os
import sys

sys.path.append(os.path.realpath(__file__))

import db

class Tr4ckDB(db.DB):
    """
    database base class for tracking, with optional dummy functionality
    
    uses the _generate_id function to categorize a packet
    """
    
    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            concurrent = True, store = True):
        db.DB.__init__(self, directory, db_mode, concurrent, enter = store)
        
        self._store = store

    def _generate_id(self, packet):
        """return the described ID for a packet"""
        raise NotImplementedError()

    def _split_id(self, id):
        """split an ID generated via self._generate_id"""
        raise NotImplementedError()
    
    def store(self, packet, mode = "wb"):
        """store the packet based on it addresses"""
        if self._store:
            return db.DB.store(self, str(packet), self._generate_id(packet),
                mode = mode)
        return

class MACDB(Tr4ckDB):
    """
    MAC-based database
    
    packets are stored in the following format:
    "source MAC -> destination MAC"
    """

    def __init__(self, *args, **kwargs):
        Tr4ckDB.__init__(self, *args, **kwargs)

    def _generate_id(self, packet):
        return ' '.join((packet.src, "->", packet.dst))

    def _split_id(self, id):
        return filter((e.strip() for e in id.split("->")))
