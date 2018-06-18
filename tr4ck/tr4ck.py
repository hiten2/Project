import os
import scapy, scapy.all # scapy.all.sniff(....)
import sys
import uuid

sys.path.append(os.path.realpath(__file__))

import geometry
import tr4ckdb

__doc__ = """
various tracking/analysis tools
from traffic analysis to host triangulation
"""

class PacketTracker(tr4ckdb.MACDB):
    """
    base class for tracking packets

    capable of concurrent database manipulation and analysis
    """
    
    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            concurrent = True, store = True, filter = lambda p: True):
        tr4ckdb.MACDB.__init__(self, directory, db_mode, concurrent, store)

        self._filter = filter
    
    def sniff(self):
        """sniff packets into the database"""
        scapy.all.sniff(prn = self._sniffer_callback)

    def _sniffer_callback(self, packet):
        if self._filter(packet):
            id = self._generate_id(packet)
            
            if self._store:
                print id, "stored to",
                self._generate_path(id, self.store(packet))
            else:
                print id

class Triangulator:
    """
    base class for triangulation

    provides triangulation internals, but no data collection functionality
    """

    def __init__(self):
        pass

    def locate(self, *circles):
        """a synonym for triangulate"""
        self.triangulate(*circles)
    
    def triangulate(self, *circles):
        """
        triangulate based on a set of circles

        algorithm:
        ????
        """
        pass

if __name__ == "__main__":
    PacketTracker("test", store = False).sniff() # test database creation
