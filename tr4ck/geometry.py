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

    def intersect(self, other):#########not done
        """determine the points of intersection with another circle"""
        euclidean_distance = self.center.euclidean_distance(other.center)
        radii_sum = self.radius + other.radius
        
        if euclidean_distance > radii_sum:
            return []
        elif euclidean_distance == radii_sum:
            pass######1 point
        pass#############2 points

class Point:
    """basic representation for a point"""

    def __init__(self, *magnitudes):
        self.magnitudes = magnitudes

    def __eq__(self, other):
        return self.magnitudes == other.magnitudes

    def euclidean_distance(self, other):
        """compute the Euclidean distance from this point to another"""
        diffs = [self.magnitudes[i] - other.magnitudes[i]
            for i in range(len(self.magnitudes))]
        return math.sqrt(sum((d ** 2 for d in diffs)))

    def slope(self, other):
        """return the 2D slope between the points"""
        assert len(self.magnitudes) == 2 and len(other.magnitudes) == 2, \
            "slope incalculable"
        xdiff = other.magnitudes[1] - self.magnitudes[1]
        ydiff = other.magnitudes[1] - self.magnitudes[1]
        return ydiff / float(xdiff)

    def __str__(self):
        return str(self.magnitudes)

class Polygon:
    """representation for a 2D polygon"""

    def __init__(self, *vertices):
        if not vertices:
            vertices = ()
        self.vertices = vertices

    def __contains__(self, point):
        pass

    def normalize(self):
        """
        remove overlapping line segments by rearranging order
        of vertices

        the resulting polygon may not be congruent to the original
        """
        high = []
        low = []
        n_vertices = len(self.vertices)
        mean_y = sum((v.magnitudes[1] for v in self.vertices))
        mean_y /= float(n_vertices)
        
        for v in self.vertices:
            if v.magnitudes[1] > mean_y:
                high.append(v)
            else:
                low.append(v)
        high = sorted(high, key = lambda v: v.magnitudes[0])
        low = sorted(low, key = lambda v: v.magnitudes[0], reverse = True)
        self.vertices = high + low

    def __str__(self):
        return str(tuple((v.magnitudes for v in self.vertices)))

if __name__ == "__main__": # testing
    p = Polygon(Point(0, 0), Point(1, 0), Point(2, 2), Point(3, 0))
    print p
    print Point(2, 2) in p
