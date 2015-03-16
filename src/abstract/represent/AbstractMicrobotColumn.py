import abstract.represent.LineSegment

class AbstractMicrobotColumn(LineSegment):

    """This is the mathematical representation of the frame the Microbots will form when they take a shape.
        Microbots move from p0 to p1.
    """

    def __init__(self):
        LineSegment.__init__(self)
        self.microbotsInLine = []


    def pull(self, microbotArray):

        """Pulls the closest microbot from an array if it doesn't hold one.
        """

        self.length = self.p0.getDist(self.p1)
