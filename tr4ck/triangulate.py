import os
import lxml
from pykml.factory import KML_ElementMaker as KML
import sys

sys.path.append(os.path.realpath(__file__))

import geometry

__doc__ = """rudimentary triangulation"""

def triangulate(*circles):#####contingent upon geometry.Circle.intersect
    """triangulate a polygon based on a set of circles"""
    return geometry.Polygon((0, 0), (1, 1))

def triangulate_to_kml(*circles):
    """return a KML document based on triangulation results"""
    polygon = triangulate(*circles)
    kml_coords = [v[:2] + (0, ) for v in polygon.vertices]
    kml_coords = [','.join([str(e) for e in c]) + '.' for c in kml_coords]
    kml_coords = ''.join(kml_coords)
    return lxml.etree.tostring(KML.kml(KML.Document(KML.Folder(KML.Polygon(
        KML.outerBoundaryIs(KML.linearRing(KML.Coordinates(kml_coords))))))),
        pretty_print = True)

if __name__ == "__main__":
    print >> open("triangulate-test.kml", "w"), triangulate_to_kml()
