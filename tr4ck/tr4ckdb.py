import os
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

    def _generate_id(self, packet):
        """return the described ID for a packet"""
        raise NotImplementedError()

    def _split_id(self, id):
        """split an ID generated via self._generate_id"""
        raise NotImplementedError()
    
    def store(self, data):
        """an intelligent wrapper for self.__setitem__"""
        if self._store:
            self[self._generate_id(data)] = str(data)

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
