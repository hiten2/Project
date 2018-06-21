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
    kml_coords = ''.join([','.join([str(e) for e in c]) + '.'
        for c in coords])
    return lxml.etree.tostring(KML.kml(KML.Document(KML.Placemark(KML.Polygon(
        KML.outerBoundaryIs(KML.linearRing(KML.Coordinates(kml_coords)))),
            KML.Style(KML.PolyStyle(KML.color(kmlcolor),
                KML.outline(outline)))))),
        pretty_print = True)

def triangulate(*circles):#####contingent upon geometry.Circle.intersect
    """triangulate a polygon based on a set of circles"""
    pass

def triangulate_to_kml(*circles):
    """return a KML document based on triangulation results"""
    return _polygon_to_kml(triangulate(*circles))

if __name__ == "__main__":
    kml = _polygon_to_kml(geometry.Polygon((-100, -100), (-100, 100),
        (100, 100), (100, -100)))
    print kml
    print >> open("triangulate-test.kml", "w"), kml
    print "Written to triangulate-test.kml"
