import point

class Ray:
    def __init__(self, org = point.Point(0, 0), dirt = 0.0):
        self.origin = org
        self.direct = dirt

    def setOrg(self, org):
        self.origin = org

    def setDirt(self, dirt):
        self.direct = dirt

    def getOrg(self):
        return self.origin

    def getDirt(self):
        return self.direct

    def prt(self):
        print "Ray: <%d, %d> (%d) -->" %(self.origin.xPos(), self.origin.yPos(), self.direct)
    

