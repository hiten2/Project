import os
import sys

sys.path.append(os.path.realpath(__file__))

import geometry
import tr4ckdb
import traffic
import triangulate

__doc__ = """
various tracking/analysis tools
from traffic analysis to host triangulation
"""

if __name__ == "__main__":
    # create a dummy database
    # and try collecting some packets into it

    # this will print source->destination MAC addresses
    db = tr4ckdb.dummy(tr4ckdb.MACDB)
    traffic.PacketTracker(db).track()

    # test triangulation over a set of circles
    circles = [geometry.Circle(geometry.Point(0, 0), 1),
        geometry.Circle(geometry.Point(0.5, 0.5), 1),
        geometry.Circle(geometry.Point(0.5, 0), 1)]
    #triangulate.Triangulator.triangulate()
