import math
import Point

class LineSegment:
    """This is the mathematical representation of the frame the Microbots will form when they take a shape.
    Microbots move from p0 to p1.
    """
    
    def __init__(self):
        self.p0 = new Point()
        self.p1 = new Point()
        self.pu = new Point()
        self.length = 0 # fine. we'll use "length."
        self.microbotsInLine = []
        
    def reevaluate(self):
        self.pu.setPoint(self.p0.getUnitVectorTo(self.p1))
        self.length = self.p0.getDist(self.p1)
        
    def setP0(self, x, y, z):
        self.p0.set(x, y, z)
        reevaluate()
        return self
        
    def setP1(self, x, y, z):
        self.p1.set(x, y, z)
        reevaluate()
        return self
        
    def getClosestPoint(self, p):
        """Gets the closest point from p on the line segment.
        """
        
        # Line is x = a + tn
        #   where a is an arbitrary point on the line
        #   and n is the unit vector to represent the direction of the line.
        # Distance is || (a-p) - ((a-p).n) x n ||
        #   where p is our point of interest.
        a_p = self.p0.subtract(p)
        a_pn = a_p.getDot(self.pu)
        a_pnxn = self.pu.multiply(a_pn)
        dist = a_p.subtract(a_pnxn).getMagnitude()
        
        # get point to the line (extending infinitely.)
        # get distance of that point to the endpoints.
        # if a distance is greater than the line segment's length, then it's outside the line segment.
        # so get the endpoint which is closer to it.
        # if not, then return that point.
