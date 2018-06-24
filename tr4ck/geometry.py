import math

__doc__ = """selective Euclidean geometry"""

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
        return math.pi * self.diameter()

    def __contains__(self, point):
        return self.center.euclidean_distance(point) <= self.radius

    def diameter(self):
        return 2 * self.radius

    def __eq__(self, other):
        return self.center == other.center and self.radius == other.radius

    def intersect(self, other):#########not done
        """determine the points of intersection with another circle"""
        euclidean_distance = self.center.euclidean_distance(other.center)
        radii_sum = self.radius + other.radius
        
        if euclidean_distance > radii_sum: # no intersection
            return []
        elif euclidean_distance == radii_sum: # 1 point of intersection
            pass
        # 2 points of intersection

        pass

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
        xdiff = other[0] - self[0]
        ydiff = other[1] - self[1]
        return ydiff / float(xdiff)

class Polygon:
    """representation for a polygon"""

    def __init__(self, *vertices):
        self.vertices = []
        
        for v in vertices: # ensure that all vertices are points
            if not isinstance(v, Point):
                v = Point(*v)
            self.vertices.append(v)
        self.vertices = tuple(self.vertices)

    def __contains__(self, ray):
        """
        2D ray casting algorithm for the point-in-polygon problem
        
        the general algorithm casts a ray towards (+) infinity
        in the X direction
        
        breakdown:
        
        count = 0
        
        for edge in polygon
            if edge isn't in domain of ray
                continue
            
            if edge isn't in range of ray
                continue
            
            if edge intersects with ray within valid range
                if intersection isn't a vertex
                    count += 1
                else if intersection wasn't previously crossed
                    count += 1
                    mark vertex as crossed
        contains = count > 0 and count isn't divisible by 2

        e.g. the upper ray (inside) intersects an odd number of times,
        whereas the lower ray (outside) intersects an even number of times
        
        +--------+   +-+
         \       |  /  |
          \  o===X=X===X===>
           +     |/     \
        o=X======X===X===X===>
         +          / \ /
          \        /   +
           +------+
        """
        count = 0
        intersected_vertices = [] # a list of intersected vertices
        
        for i in range(len(self.vertices)):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % len(self.vertices)] # allow wrap-around
            
            if max(a[0], b[0]) < ray[0]: # bad domain
                continue
            
            if ray[1] < min(a[1], b[1]) or ray[1] > max(a[1], b[1]):
                continue # bad range
            
            if a[0] == b[0]: # edge is vertical, so ray intersects
                count += 1
            else:
                intersect = Point((ray[1] - a[1]) / a.slope(b) + a[0], ray[1])
                
                if intersect[0] >= ray[0]:
                    if not intersect in self.vertices:
                        count += 1
                    elif not intersect in intersected_vertices:
                        count += 1
                        intersected_vertices.append(intersect)
        return count and count % 2

    def __eq__(self, other):
        return self.vertices == other.vertices

    def normalize(self):
        """
        remove overlapping 2D edges by rearranging order
        of vertices as such:
        1. split into two halves by Y-value
        2. sort upper half by X-values, from least to greatest
        3. sort lower half by X-values, from greatest to least
        4. new vertices = upper half + lower half
        
        the resulting polygon may not be congruent to the original

        e.g. Polygon((0, 0), (1, 1), (0, 1), (1, 0))
            -> Polygon((0, 1), (1, 1), (1, 0), (0, 0))

        +----+           +----+
         \  /            |    |
          \/             |    |
          /\     --->    |    |
         /  \            |    |
        +----+           +----+
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
        self.vertices = tuple(high + low)

    def __str__(self):
        return str(tuple(self.vertices))
