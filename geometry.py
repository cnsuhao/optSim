import math

class Point:
    def __init__(self, xpos = 0.0, ypos = 0.0):
        self.x = xpos
        self.y = ypos

    def shift(self, vec):
        return Point(self.x + vec.u, self.y + vec.v)

    def distance(self, pt):
        return math.sqrt((pt.x - self.x) ** 2 + (pt.y - self.y) ** 2)

    def prt(self):
        print "Point: <%d, %d>" %(self.x, self.y) 

class Vector:
    def __init__(self, u = 1.0, v = 0.0):
        self.u = u
        self.v = v

    def __add__(self, other):
        return Vector(self.u + other.u, self.v + other.v)

    def __sub__(self, other):
        return Vector(self.u - other.u, self.v - other.v)

    def __mul__(self, other):
        return Vector(self.u * other.u, self.v * other.v)

    def angle(self):    # radius
        return math.atan2(self.u, self.v)

    def prt(self):
        print "Vector: <0, 0> --> <", self.u, ", ", self.v, ">" 


class Ray:
    def __init__(self, org = Point(0, 0), dirt = Vector()):
        self.origin = org
        self.direct = dirt

    def toLine(self):
        end_point = self.origin.shift(self.direct)
        return Line(self.origin, end_point)

    def prt(self):
        print "Ray: <%d, %d> (%d) -->" %(self.origin.x, self.origin.y, self.direct)
    

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

    def prt(self):
        pass


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

    def prt(self):
        print "Line Segment: <%d, %d> -- <%d, %d>" %(self.start.x, self.start.y, self.end.x, self.end.y)


