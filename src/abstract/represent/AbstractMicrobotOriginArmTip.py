class AbstractMicrobotOriginArmTip:

    """This is the mathematical representation of a Microbot.
        Each Microbot consists of two arms of equal length hinged on a spherical center.
        The representation can take different configurations, concerning the origin point of the object.
        The origin point of a Microbot object is the tip of one arm;
            when the Microbot moves, it will be as if it is pulled from this origin point,
            while the rest of it realigns as if on ragdoll physics.
        A concrete representation must be implemented that takes this representations' configurations
            and translates it into armature positioning.
    """

    def __init__(self, span, cx=0, cy=0, cz=0, rz=0, rx=0, ry=0):
        # This is the length of the Microbot.
        # Cannot use term "length" to avoid confusion with data types.
        self.span = span

        # Original Orientation:
        #     Rotation: pointing at Y+
        #     Center: (0, 0, 0)
        # Origin Point

        self.o = new Point(cx, cy-span/2, cz)
        # Center Point
        self.c = new Point(cx, cy, cz)

        # Tail Point
        self.t = new point(cx, cy+span/2, cz)

    def getArmTipDist(self, p):
        d1 = self.o.getDist(p)
        d2 = self.t.getDist(p)
        return min(d1, d2)

    def pull(self, p2):
         """ Pulls the Microbot from its origin.
            Development incompleteness:
            - does not cover cases when the distance from tail to p2 is less than twice the Microbot's length.
            (In this situation, if the Microbot forms a triangle, a triangle rotation or stretching may be done instead of simply pulling its center and tail points.       
        """

        self.o.setPoint(p2)
        self.c.setDistFrom(self.o, span)
        self.t.setDistFrom(self.c, span)

    def flip(self):
        """ Switches the origin point with the tail point.
        """

        medium = new Point().setPoint(self.o)
        self.o.setPoint(self.t)
        self.t.setPoint(medium)

    @staticmethod
    def pullClosestMicrobot(microbotPool, p):
        """Finds the Microbot whose origin or tail is closest to p.
        """

        closestBot = None
        closestIndex = None
        closestDist = float("inf")

        for i, y in enumerate(microbotPool):
            dist = y.getArmTipDist(p)
            if (dist<closestDist):
                closestBot = y
                closestIndex = i
                closestDist = dist

        return [closestBot, closestIndex, closestDist]
