"""
Run this code by importing it into the Python console for Blender.

Here's a sample of lines that you can use if you want to test things around.

------
from apmiiib.demo.microbotsimulation.SpikeDemonstration import microbotAbstraction, actors, spike
from apmiiib.abstract.represent.microbot.MicrobotSpikeParametrics import MicrobotSpikeParametrics
from apmiiib.abstract.geom.Point import Point

spike.setThreadParametrics(MicrobotSpikeParametrics.SQUARE)
spike.reshape(threads=25) != None

spike.reshape(direction=Point(0,0,1)) != None

def f2(self, r, t, z):
	return r+z*0.10

spike.reshape(shape=f2, direction=Point(0,1,1), threads=300) != None

------

"""



from apmiiib.demo.microbotsimulation.MicrobotFactory import MicrobotFactory
from apmiiib.abstract.represent.microbot.AbstractMicrobotOriginArmTip import AbstractMicrobotOriginArmTip
from apmiiib.abstract.represent.microbot.AbstractMicrobotBasicSpike import AbstractMicrobotBasicSpike
from apmiiib.abstract.represent.microbot.AbstractMicrobotLineup import AbstractMicrobotLineup
from apmiiib.abstract.represent.microbot.MicrobotSpikeParametrics import MicrobotSpikeParametrics
from apmiiib.world.represent.ActorMicrobotOriginArmTip import ActorMicrobotOriginArmTip
from apmiiib.abstract.geom.Point import Point

# Constants/Parameters

microbotLimit = 1000
microbotThreads = 250
radiusHeightRatio = 0.25
spikeDirection = Point(0, 1, 1)
spikeBasePoint = Point(0, 0, 0)

microbotLimit2 = 0
#microbotThreads2 = 250
#radiusHeightRatio2 = 0.25
#spikeDirection2 = Point(0, 0, 1)
#spikeBasePoint2 = Point(0, 1, 0)

def spikeShape(self, r, t, z):
	return z*0.15+r

microbotSpan = 0.1
microbotBreadth = 2*microbotSpan/10.55

# First, we only want to ensure that there are N Microbots.

while (MicrobotFactory.getArmature(microbotLimit+microbotLimit2) == None):
	MicrobotFactory.create()

# Create the same number of abstractions.
# Store in a list of said abstractions.
		
actors = []
microbotAbstraction = AbstractMicrobotLineup()
for i in range(0,microbotLimit+microbotLimit2):
	abstraction = AbstractMicrobotOriginArmTip(microbotSpan, 0, 0, 0, 0, 0, 0)
	microbotAbstraction.append(abstraction)
	actors.append(ActorMicrobotOriginArmTip(abstraction, MicrobotFactory.getArmature(i+1)))

# Create a spike.
spike = AbstractMicrobotBasicSpike(radiusHeightRatio, microbotSpan, microbotBreadth, spikeShape)
#spike2 = AbstractMicrobotBasicSpike(radiusHeightRatio2, microbotSpan, microbotBreadth, spikeShape)

# CALCULATE THE MICROBOT FORMATION
# It outputs a list of abstractions it worked with.

spike.reshape(spikeShape, spikeBasePoint, spikeDirection, microbotThreads, microbotAbstraction, microbotLimit)
#spike2.reshape(spikeShape, spikeBasePoint2, spikeDirection2, microbotThreads2, microbotAbstraction, microbotLimit2)
	
actors[0].armature.hide = False
actors[0].armature.select = True
