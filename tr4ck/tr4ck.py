import os
import scapy, scapy.all # scapy.all.sniff(....)
import sys
import uuid

sys.path.append(os.path.realpath(__file__))

import tr4ckdb

class PacketTracker(tr4ckdb.MACDB):
    """
    base class for tracking packets

    capable of concurrent database manipulation and analysis
    """

    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            concurrent = True, filter = lambda p: True, store = True):
        tr4ckdb.MACDB.__init__(self, directory, db_mode, concurrent)

        self._filter = filter
        self._store = store
    
    def sniff(self):
        """sniff packets into the database"""
        scapy.all.sniff(prn = self._sniffer_callback)

    def _sniffer_callback(self, packet):
        if self._filter(packet):
            id = self._generate_id(packet)

            if self._store:
                print id, "stored to",
                print self._generate_path(id, self.store(packet))

if __name__ == "__main__":
    PacketTracker("test", store = False).sniff() # test database creation
