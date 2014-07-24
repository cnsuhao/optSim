'''
Created on Jul 23, 2014

@author: andy

Description:
    The radian range is [0, 2pi)

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

    def distanceTo(self, pt):
        return math.sqrt((pt.x - self.x) ** 2 + (pt.y - self.y) ** 2)

    def __eq__(self, pt):
        return self.x == pt.x and self.y == pt.y

    def __str__(self):
        string = "Point: <%s, %s>" % (self.x, self.y) 
        return string

    def __repr__(self):
        string = "Point: <%s, %s>" % (self.x, self.y) 
        return string

class Ray:
    origin = Point()
    radian = 0.0
    
    def __init__(self, org=Point(0, 0), rad=0.0):
        self.origin = org
        self.radian = rad

    def toLine(self):
        end_point = Point(self.origin.x + math.cos(self.radian), self.origin.y + math.sin(self.radian))
        return Line(self.origin, end_point)

    def __eq__(self, other):
        return self.origin == other.origin and self.radian == other.radian

    def __str__(self):
        string = "Ray: <%s, %s> (%s) -->" % (self.origin.x, self.origin.y, self.radian)
        return string
    
    def __repr__(self):
        string = "Ray: <%s, %s> (%s) -->" % (self.origin.x, self.origin.y, self.radian)
        return string

class Line:
    point1 = Point()
    point2 = Point()
    
    def __init__(self, pt1=Point(0, 0), pt2=Point(1, 1)):
        if pt1 == pt2:
            raise ArithmeticError, "invalid Line: %s" % self
        else:
            self.point1 = pt1
            self.point2 = pt2

    def intersectPoint(self, line):
        a = self.point1
        b = self.point2
        c = line.point1
        d = line.point2

        if self.slope() == line.slope():
            print "The two lines are parrelled!"
            return None
        else:
            ipt = Point()
            ipt.x = ((b.x - a.x) * (c.x - d.x) * (c.y - a.y) - c.x * (b.x - a.x) * (c.y - d.y) + a.x * (b.y - a.y) * (c.x - d.x)) / ((b.y - a.y) * (c.x - d.x) - (b.x - a.x) * (c.y - d.y))
            ipt.y = ((b.y - a.y) * (c.y - d.y) * (c.x - a.x) - c.y * (b.y - a.y) * (c.x - d.x) + a.y * (b.x - a.x) * (c.y - d.y)) / ((b.x - a.x) * (c.y - d.y) - (b.y - a.y) * (c.x - d.x))
            return ipt

    def slope(self):
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)

    def parallelWith(self, line):
        return self.slope() == line.slope

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
    
    def radian(self):
        delta_x = self.end.x - self.start.x
        delta_y = self.end.y - self.start.y
        if delta_x == 0:
            if delta_y > 0:
                return math.pi / 2
            elif delta_y < 0:
                return math.pi * 3 / 4
            else
                raise ArithmeticError, "wrong LineSeg: %s" %self
        
        rad = math.atan(math.fabs(self.v) / math.fabs(self.u))
        if delta_x > 0 and delta_y > 0:  # first quadrant
            return rad
        elif delta_x < 0 and delta_y > 0:  # second quadrant
            return math.pi - rad
        elif delta_x < 0 and delta_y < 0:  # third quadrant
            return math.pi + rad
        else:  # forth quadrant
            return 2 * math.pi - rad

    def hasPoint(self, pt):
        ac = self.length()
        ab = self.start.distanceTo(pt)
        bc = pt.distanceTo(self.end)
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

