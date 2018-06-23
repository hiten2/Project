import os
import lxml
from pykml.factory import KML_ElementMaker as KML
import sys

sys.path.append(os.path.realpath(__file__))

import geometry

__doc__ = """rudimentary triangulation"""

def _polygon_to_kml(polygon, kmlcolor = "ff0000ff", outline = 0):###problematic
    """return the KML equivalent for a geometry.Polygon"""
    coords = [v[:2] + (0, ) for v in polygon.vertices] # lat./long. only
    kml_coords = '\n' + '\n'.join([','.join([str(e) for e in c]) + '.' + '\n'
        for c in coords])
    return ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        + lxml.etree.tostring(KML.kml(KML.PlaceMark(KML.Polygon(KML.extrude(1),
            KML.altitudeMode("relativeToGround"), KML.outerBoundaryIs(
                KML.LinearRing(KML.coordinates(kml_coords)))))),
        pretty_print = True))

def triangulate(*circles):#####contingent upon geometry.Circle.intersect
    """triangulate a polygon based on a set of circles"""
    pass

def triangulate_to_kml(*circles):
    """return a KML document based on triangulation results"""
    return _polygon_to_kml(triangulate(*circles))

if __name__ == "__main__":
    kml = _polygon_to_kml(geometry.Polygon((-1, -1), (-1, 1),
        (1, 1), (1, -1)))
    print kml
    print >> open("triangulate-test.kml", "w"), kml
    print "Written to triangulate-test.kml"
