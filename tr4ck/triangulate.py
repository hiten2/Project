import os
import sys

sys.path.append(os.path.realpath(__file__))

import geometry

__doc__ = """rudimentary trangulation"""

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
        1. determine intersections and their overlap
        2. remove outlying intersections
        3. points of intersection + overlap -> rectangles
        4. return the polygon formed by the overlapping rectangles
        """
        pass
