'''
Created on Jul 23, 2014

@author: andy

Description:
    The radius range is [0, 2pi)

'''
import math

class Point:
    x = 0.0
    y = 0.0
    
    def __init__(self, xpos=0.0, ypos=0.0):
        self.x = xpos * 1.0  # to float
        self.y = ypos * 1.0

    def shift(self, vec):
        return Point(self.x + vec.u, self.y + vec.v)

    def distance(self, pt):
        return math.sqrt((pt.x - self.x) ** 2 + (pt.y - self.y) ** 2)

    def __eq__(self, pt):
        return self.x == pt.x and self.y == pt.y

    def __str__(self):
        string = "Point: <%s, %s>" % (self.x, self.y) 
        return string

    def __repr__(self):
        string = "Point: <%s, %s>" % (self.x, self.y) 
        return string

class Vector:
    u = 0.0
    v = 0.0
    
    def __init__(self, u=1.0, v=0.0):
        self.u = u * 1.0  # to float
        self.v = v * 1.0    

    def __add__(self, other):
        return Vector(self.u + other.u, self.v + other.v)

    def __sub__(self, other):
        return Vector(self.u - other.u, self.v - other.v)

    def __neg__(self):
        return Vector(-self.u, -self.v)

    def __mul__(self, other):
        if isinstance(other, Vector):  # dot mul
            return self.u * other.u + self.v * other.v
        else:
            return Vector(self.u * other, self.v * other)

    def __eq__(self, other):
        return self.angle(other) == 0

    def toRadius(self):    
        if self.u == 0:
            if self.v > 0:
                return math.pi / 2
            elif self.v < 0:
                return math.pi * 3 / 4
            else:
                raise ArithmeticError, "wrong Vector: %s" % self
        
        rad = math.atan(math.fabs(self.v) / math.fabs(self.u))   
        if self.u > 0 and self.v > 0:  # first quadrant
            return rad
        elif self.u < 0 and self.v > 0:  # second quadrant
            return math.pi - rad
        elif self.u < 0 and self.v < 0:  # third quadrant
            return math.pi + rad
        else:  # forth quadrant
            return 2 * math.pi - rad

    @staticmethod
    def fromRadius(radius):
        return Vector(math.cos(radius), math.sin(radius))

    def mod(self):
        return Point(self.u, self.v).distance(Point(0, 0))

    # [0, 2pi)
    def angle(self, vec):
        rad1 = self.toRadius()
        rad2 = vec.toRadius()
        delta = rad1 - rad2
        if delta > 0:
            return 2 * math.pi - delta
        else:  # <= 0
            return math.fabs(delta) 

    def __str__(self):
        string = "Vector: --> <%s, %s>" % (self.u, self.v)
        return string

    def __repr__(self):
        string = "Vector: --> <%s, %s>" % (self.u, self.v)
        return string

class Ray:
    origin = Point()
    direct = Vector()
    
    def __init__(self, org=Point(0, 0), dirt=Vector()):
        self.origin = org
        self.direct = dirt

    def toLine(self):
        end_point = self.origin.shift(self.direct)
        return Line(self.origin, end_point)

    def __eq__(self, other):
        return self.origin == other.origin and self.direct == other.origin

    def __str__(self):
        string = "Ray: <%s, %s> (%s) -->" % (self.origin.x, self.origin.y, self.direct)
        return string
    
    def __repr__(self):
        string = "Ray: <%s, %s> (%s) -->" % (self.origin.x, self.origin.y, self.direct)
        return string

class Line:
    point1 = Point()
    point2 = Point()
    
    def __init__(self, pt1=Point(0, 0), pt2=Point(1, 1)):
        if pt1 == pt2:
            raise ArithmeticError, "invalid Line: %s" %self
        else:
            self.point1 = pt1
            self.point2 = pt2

    def intersectPoint(self, line):
        a = self.point1
        b = self.point2
        c = line.point1
        d = line.point2

        if (b.y - a.y) * (c.x - d.x) - (b.x - a.x) * (c.y - d.y) == 0:
            print "the two lines are parrelled!"
            return None
        else:
            ipt = Point()
            ipt.x = ((b.x - a.x) * (c.x - d.x) * (c.y - a.y) - c.x * (b.x - a.x) * (c.y - d.y) + a.x * (b.y - a.y) * (c.x - d.x)) / ((b.y - a.y) * (c.x - d.x) - (b.x - a.x) * (c.y - d.y))
            ipt.y = ((b.y - a.y) * (c.y - d.y) * (c.x - a.x) - c.y * (b.y - a.y) * (c.x - d.x) + a.y * (b.x - a.x) * (c.y - d.y)) / ((b.x - a.x) * (c.y - d.y) - (b.y - a.y) * (c.x - d.x))
            return ipt

    def slope(self):
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)

    def __eq__(self, other):
        v1 = Vector(self.point2.x, self.point2.y) - Vector(self.point1.x, self.point1.y)
        v2 = Vector(other.point2.x, other.point2.y) - Vector(other.point1.x, other.point1.y)
        return v1 == v2 or v1 == -v2

    def __str__(self):
        string = "Line: -- <%s, %s> -- <%s, %s> --" % (self.point1.x, self.point1.y, self.point2.x, self.point2.y)
        return string

    def __repr__(self):
        string = "Line: -- <%s, %s> -- <%s, %s> --" % (self.point1.x, self.point1.y, self.point2.x, self.point2.y)
        return string


class LineSeg:
    start = Point()
    end = Point()
    
    def __init__(self, pt1=Point(0, 0), pt2=Point(1, 1)):
        if pt1 == pt2:
            raise ArithmeticError, "invalid LineSeg: %s" % self
        else:
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
        string = "Line Segment: <%s, %s> -- <%s, %s>" % (self.start.x, self.start.y, self.end.x, self.end.y)
        return string

    def __repr__(self):
        string = "Line Segment: <%s, %s> -- <%s, %s>" % (self.start.x, self.start.y, self.end.x, self.end.y)
        return string

