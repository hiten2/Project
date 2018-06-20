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

class Point(tuple):
    """basic representation for a point"""

    def __new__(_class, *magnitudes):
        return tuple.__new__(_class, magnitudes)

    def euclidean_distance(self, other):
        """compute the Euclidean distance from this point to another"""
        diffs = [self[i] - other[i]
            for i in range(len(self))]
        return math.sqrt(sum((d ** 2 for d in diffs)))
    
    def slope(self, other):
        """return the 2D slope between the points"""
        assert len(self) == 2 and len(other) == 2, "slope incalculable"
        xdiff = other[1] - self[1]
        ydiff = other[1] - self[1]
        return ydiff / float(xdiff)

class Polygon:
    """representation for a 2D polygon"""

    def __init__(self, *vertices):
        self.vertices = []
        
        for v in vertices: # ensure that all vertices are points
            if not isinstance(v, Point):
                v = Point(*v)
            self.vertices.append(v)
        self.vertices = tuple(self.vertices)

    def __contains__(self, point):#############seems to work, but questionable
        """
        ray casting algorithm for the point-in-polygon problem
        
        the general algorithm casts a ray towards (+) infinity
        in the X direction
        
        breakdown:
        
        count = 0
        
        for edge in polygon
            if edge isn't in the direction (X or Y) the ray casts
                continue
            
            if edge intersects within valid range
                count += 1
        contains = count > 0 and count isn't divisible by 2
        """
        nintersects = 0
        ray_y = point[1]
        
        for i in range(len(self.vertices)):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % len(self.vertices)] # allow wrap-around
            
            if max(a[0], b[0]) < point[0]: # bad domain
                continue
            
            if ray_y < min(a[1], b[1]) or ray_y > max(a[1], b[1]): # bad range
                continue
            
            try:
                m = a.slope(b)
            except ZeroDivisionError: # vertical line
                nintersects += 1
                continue
            leftmost = sorted((a, b), key = lambda p: p[0])[0]
            eq_y_at_point = m * (point[0] - a[0]) + a[1]

            if leftmost[1] <= ray_y and eq_y_at_point <= ray_y:
                nintersects += 1
        return nintersects and nintersects % 2

    def normalize(self):
        """
        remove overlapping line segments by rearranging order
        of vertices as such:
        1. split into two halves by Y-value
        2. sort upper half by X-values, from least to greatest
        3. sort lower half by X-values, from greatest to least
        4. new vertices = upper half + lower half
        
        the resulting polygon may not be congruent to the original
        """
        high = []
        low = []
        n_vertices = len(self.vertices)
        mean_y = sum((v[1] for v in self.vertices))
        mean_y /= float(n_vertices)
        
        for v in self.vertices:
            if v[1] > mean_y:
                high.append(v)
            else:
                low.append(v)
        high = sorted(high, key = lambda v: v[0])
        low = sorted(low, key = lambda v: v[0], reverse = True)
        self.vertices = high + low

    def __str__(self):
        return str(self.vertices)

if __name__ == "__main__": # testing
    p = Point(2, 2)
    polygon = Polygon(Point(0, 0), Point(0, 1), Point(2, 2), Point(3, 1))
    print p, "in", polygon, '?'
    print p in polygon
