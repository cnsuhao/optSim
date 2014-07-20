import math

class Point:
    def __init__(self, xpos = 0.0, ypos = 0.0):
        self.x = xpos
        self.y = ypos

    def setX(self, xpos):
        self.x = xpos

    def setY(self, ypos):
        self.y = ypos

    def xPos(self):
        return self.x

    def yPos(self):
        return self.y

    def angleToPoint(self, pt):
        return math.atan2(pt.yPos() - self.y, pt.xPos() - self.x)

    def distanceTo(self, sth):
        import ray
        if isinstance(sth, Point):
            return math.sqrt((sth.xPos() - self.x) ** 2 + (sth.yPos() - self.y) ** 2)
        elif isinstance(sth, ray.Ray):
            beta = self.angleToPoint(sth.origin)
            delta_angle = beta - sth.direct
            return math.sin(delta_angle) * self.distanceTo(sth.origin)
        else:   # line or line segment
            agl = sth.getPt1.angleToPoint(sth.getPt2)
            ray = ray.Ray(sth.getPt1, agl)
            return self.distanceTo(ray)

    def prt(self):
        print "Point: <%d, %d>" %(self.x, self.y) 
