import point

class Line:
    def __init__(self, pt1 = point.Point(0, 0), pt2 = point.Point(1, 1)):
        self.point1 = pt1
        self.point2 = pt2

    def setPt1(self, pt1):
        self.point1 = pt1

    def setPt2(self, pt2):
        self.point2 = pt2

    def getPt1(self):
        return self.point1

    def getPt2(self):
        return self.point2

    def intersectWith(self, sth):
        import ray
        import lineseg
        if isinstance(sth, point.Point):
            if sth.distanceTo(self) == 0:
                return sth
            else:
                return None
        elif isinstance(sth, ray.Ray):




    def prt(self):
        print "Line: -- <%d, %d> -- <%d, %d> -- " %(self.point1.xPos(), self.point1.yPos(), self.point2.xPos(), self.point2.yPos())


