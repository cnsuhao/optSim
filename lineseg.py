import math
import point

class LineSeg:
    def __init__(self, pt1 = point.Point(0, 0), pt2 = point.Point(1, 1)):
        self.point1 = pt1
        self.point2 = pt2

    def length(self):
        return math.sqrt((self.point2.xPos() - self.point1.xPos()) ** 2 + (self.point2.yPos() - self.point1.yPos()) ** 2)

    def setPt1(self, pt1):
        self.point1 = pt1

    def setPt2(self, pt2):
        self.point2 = pt2

    def getPt1(self):
        return self.point1

    def getPt2(self):
        return self.point2

    def prt(self):
        print "Line Segment: <%d, %d> -- <%d, %d>" %(self.point1.xPos(), self.point1.yPos(), self.point2.xPos(), self.point2.yPos())


