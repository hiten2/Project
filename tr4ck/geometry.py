import math

__doc__ = """geometry"""

class Circle:
    """circle representation"""

    def __init__(self, center = None, radius = 1):
        if not center:
            center = Point(0, 0)
        self.center = center
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def circumference(self):
        return math.pi * 2 * self.radius

    def __contains__(self, point):
        return self.center.euclidean_distance(point) <= self.radius

    def intersect(self, other):
        """determine the points of intersection with another circle"""
        pass

class Point:
    """basic representation for a point"""

    def __init__(self, *magnitudes):
        self.magnitudes = magnitudes

    def euclidean_distance(self, other):
        """compute the Euclidean distance from this point to another"""
        diffs = [self.magnitudes[i] - other.magnitudes[i]
            for i in range(len(self.magnitudes))]
        return math.sqrt(sum((d ** 2 for d in diffs)))

class Polygon:
    """representation for a polygon"""

    def __init__(self, vertices = None):
        if not vertices:
            vertices = []
        self.vertices = vertices

    def __contains__(self, point):
        pass
