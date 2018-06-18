import os
import sys

sys.path.append(os.path.realpath(__file__))

import tr4ckdb
import traffic
import triangulate

__doc__ = """
various tracking/analysis tools
from traffic analysis to host triangulation
"""

if __name__ == "__main__":
    traffic.PacketTracker(tr4ckdb.MACDB("test", store = False)).track()
