import geometry

class Light(Ray):
    def __init__(self, intensity = 1.0, org = Point(0, 0), dirt = 0.0):
        self.intensity = intensity
        Ray.__init__(org, dirt)

    def incidencePoint(self, interface):
        line1 = self.toLine()
        line2 = interface.toLine()
        ipt = line1.intersectPoint(line2)
        if ipt != None and interface.hasPoint(ipt):
            return ipt
        else:
            return None

    def postLightSource(self, interface, inpoint):
       norm_slope = -1.0 / interface.slope() 
       norm_vector = geometry.Vector.fromRadius(math.atan(norm_slope))
       light_vector = self.direct
       if light_vector.angle(norm_vector) > 3.14 / 2:
           norm_vector = geometry.Vector.fromRadius(math.atan(norm_slope) + 3.14)

        
class Interface(LineSeg):
    def __init__(self, up_refidx = 1.0, down_refidx = 1.0, pt1 = Point(0,0), pt2 = Point(1,1)):
        self.up_refidx = up_refidx
        self.down_refidx = down_refidx
        LineSeg.__init__(pt1, pt2)

class LightSource:
    def __init__(self):
        pass

    def generate(self):
        pass
