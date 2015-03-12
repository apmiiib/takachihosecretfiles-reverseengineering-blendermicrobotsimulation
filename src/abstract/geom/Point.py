import math

class Point:

    def __init__(self, x=0, y=0 , z=0):

        self.x = x

        self.y = y

        self.z = z

    def set(self, x, y, z):

        self.x = x

        self.y = y

        self.z = z

        return self

    def setPoint(self, p2):

        self.x = p2.x

        self.y = p2.y

        self.z = p2.z

        return self

    def getDist(self, p2):

        x = self.x-p2.x

        y = self.y-p2.y

        z = self.z-p2.z

        return sqrt(x*x+y*y+z*z)

    def getUnitVectorTo(self, p2):

        dist = self.getDist(p2)

        x = p2.x-self.x

        y = p2.y-self.y

        z = p2.z-self.z

        return new Point(x/dist, y/dist, z/dist)

    def setDistFrom(self, p2, dist):

        """Moves this point so the distance from this point to another point is as specified.

            Preserves their relative angle.

            That is to say, any position translation will be along the line drawn by self and p2.

        """

        dist0 = getDist(p2)

        self.x = p2.x-(p2.x-self.x)/dist0*dist

        self.y = p2.y-(p2.y-self.y)/dist0*dist

        self.z = p2.z-(p2.z-self.z)/dist0*dist
