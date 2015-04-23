from apmiiib.demo.microbotsimulation.MicrobotFactory import MicrobotFactory
from apmiiib.abstract.represent.microbot.AbstractMicrobotOriginArmTip import AbstractMicrobotOriginArmTip
from apmiiib.abstract.represent.microbot.AbstractMicrobotBasicSpike import AbstractMicrobotBasicSpike
from apmiiib.world.represent.ActorMicrobotOriginArmTip import ActorMicrobotOriginArmTip
from apmiiib.abstract.geom.Point import Point

# Constants/Parameters

microbotLimit = 800
microbotThreads = 100
radiusHeightRatio = 0.25
spikeDirection = Point(0, 1, 1)
spikeBasePoint = Point(0, 0, 0)

def spikeShape(self, r, t, z):
	return z*0.15+r

microbotSpan = 0.1
microbotBreadth = 2*microbotSpan/10.55

# First, we only want to ensure that there are N Microbots.

while (MicrobotFactory.getArmature(microbotLimit) == None):
	MicrobotFactory.create()

# Create the same number of abstractions.
# Store in a list of said abstractions.

class AbstractMicrobotLineup:
	def __init__(self):
		self.array = []
		self.roverIndex = 0;
		
	def append(self, value):
		self.array.append(value)
		
	def getOneOriginArmTip(self):
		output = self.array[self.roverIndex];
		self.roverIndex += 1
		if (self.roverIndex == len(self.array)):
			self.roverIndex = 0
		return output
		
microbotAbstraction = AbstractMicrobotLineup()
	
for i in range(0,microbotLimit):
	microbotAbstraction.append(AbstractMicrobotOriginArmTip(microbotSpan, 0, 0, 0, 0, 0, 0))

# Create a spike.

spike = AbstractMicrobotBasicSpike(spikeBasePoint, spikeDirection, radiusHeightRatio, microbotSpan, microbotBreadth, spikeShape)

# CALCULATE THE MICROBOT FORMATION
# It outputs a list of abstractions it worked with.

abstractions = spike.calculate(microbotAbstraction, microbotLimit, microbotThreads)

# For each abstraction, assign an actor, then update.
actors = []
ith = 0
for i in abstractions:
	actors.append(ActorMicrobotOriginArmTip(i, MicrobotFactory.getArmature(ith+1)).update())
	ith += 1
	
actors[0].armature.hide = False
actors[0].armature.select = True

def reshapeSpike(_spike=spike, _spikeShape=spikeShape, _spikeDirection=None, threads=microbotThreads, abstraction=microbotAbstraction, lim=microbotLimit):
	_spike.spikeShape = _spikeShape
	if (_spikeDirection != None):
		_spike.spikeDirection = _spikeDirection
	abstractions = spike.calculate(abstraction, lim, threads)
	for i in abstractions:
		i.being.update()
		
