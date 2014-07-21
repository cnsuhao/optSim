import math

class Point:
    def __init__(self, xpos = 0.0, ypos = 0.0):
        self.x = xpos
        self.y = ypos

    def shift(self, vec):
        return Point(self.x + vec.u, self.y + vec.v)

    def distance(self, pt):
        return math.sqrt((pt.x - self.x) ** 2 + (pt.y - self.y) ** 2)

    def __str__(self):
        str = "Point: <%s, %s>" %(self.x, self.y) 
        return str

    def __repr__(self):
        str = "Point: <%s, %s>" %(self.x, self.y) 
        return str

class Vector:
    def __init__(self, u = 1.0, v = 0.0):
        self.u = u
        self.v = v

    def __add__(self, other):
        return Vector(self.u + other.u, self.v + other.v)

    def __sub__(self, other):
        return Vector(self.u - other.u, self.v - other.v)

    def __mul__(self, other):
        if isinstance(other, Vector):   # dot mul
            return self.u * other.u + self.v * other.v
        else:
            return Vector(self.u * other, self.v * other)

    def toRadius(self):    
        return math.atan2(self.u, self.v)

    @staticmethod
    def fromRadius(radius):
        return Vector(math.cos(radius), math.sin(radius))

    def mod(self):
        return Point(self.u, self.v).distance(Point(0, 0))

    def angle(self, vec):
        cos_val = self.__mul__(vec) / (self.mod() * vec.mod())
        return math.acos(cos_val)

    def __str__(self):
        str = "Vector: --> <%s, %s>" %(self.u, self.v)
        return str

    def __repr__(self):
        str = "Vector: --> <%s, %s>" %(self.u, self.v)
        return str

class Ray:
    def __init__(self, org = Point(0, 0), dirt = Vector()):
        self.origin = org
        self.direct = dirt

    def toLine(self):
        end_point = self.origin.shift(self.direct)
        return Line(self.origin, end_point)

    def __str__(self):
        str = "Ray: <%s, %s> (%s) -->" %(self.origin.x, self.origin.y, self.direct)
        return str
    
    def __repr__(self):
        str = "Ray: <%s, %s> (%s) -->" %(self.origin.x, self.origin.y, self.direct)
        return str

class Line:
    def __init__(self, pt1 = Point(0, 0), pt2 = Point(1, 1)):
        self.point1 = pt1
        self.point2 = pt2

    def intersectPoint(self, line):
        a = self.point1
        b = self.point2
        c = line.point1
        d = line.point2

        if (b.x - a.y) * (c.x - d.x) - (b.x - a.x) * (c.y - d.y) == 0:
            print "the two lines are parrelled!"
            return None
        else:
            ipt = Point()
            ipt.x = ((b.x - a.x) * (c.x - d.x) * (c.y - a.y) - c.x * (b.x - a.x) * (c.y - d.y) + a.x * (b.y - a.y) * (c.x - d.x)) / ((b.y - a.y) * (c.x - d.x) - (b.x - a.x) * (c.y - d.y))
            ipt.y = ((b.y - a.y) * (c.y - d.y) * (c.x - a.x) - c.y * (b.y - a.y) * (c.x - d.x) + a.y * (b.x - a.x) * (c.y - d.y)) / ((b.x - a.x) * (c.y - d.y) - (b.y - a.y) * (c.x - d.x))
            return ipt

    def slope(self):
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)

    def __str__(self):
        str = "Line: -- <%s, %s> -- <%s, %s> --" %(self.point1.x, self.point1.y, self.point2.x, self.point2.y)
        return str

    def __repr__(self):
        str = "Line: -- <%s, %s> -- <%s, %s> --" %(self.point1.x, self.point1.y, self.point2.x, self.point2.y)
        return str


class LineSeg:
    def __init__(self, pt1 = Point(0, 0), pt2 = Point(1, 1)):
        # pt1 can't equal to pt2
        self.start = pt1
        self.end = pt2

    def length(self):
        return math.sqrt((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2)

    def hasPoint(self, pt):
        ac = self.length()
        ab = self.start.distance(pt)
        bc = pt.distance(self.end)
        if ac == ab + bc:
            return True
        else:
            return False

    def toLine(self):
        return Line(self.start, self.end)

    def __str__(self):
        str = "Line Segment: <%s, %s> -- <%s, %s>" %(self.start.x, self.start.y, self.end.x, self.end.y)
        return str

    def __repr__(self):
        str = "Line Segment: <%s, %s> -- <%s, %s>" %(self.start.x, self.start.y, self.end.x, self.end.y)
        return str

