from apmiiib.abstract.geom.Point import Point
from math import pi, floor, pow

class AbstractMicrobotBasicSpike:
	"""This class builds a construct of Microbots that form a spike.
	This uses a technique normally used for A* search in determining the order
		of Microbots that would be set in place.
	"""
	
	def defaultSpikeShape(self, r, t, z):
		""" Takes a polar-coordinate and height value and returns its weight.
		The Microbot placement algorithm prioritizes points with smaller weights first.
		"""
		
		return r*self.radiusHeightRatio+z
		
	
	def __init__(self, basePoint, spikeDirection, radiusHeightRatio, microbotSpan, microbotBreadth, spikeShape=None):
		self.basePoint = basePoint
		self.spikeDirection = spikeDirection.getDirection()
		self.radiusHeightRatio = radiusHeightRatio
		self.microbotSpan = microbotSpan
		self.microbotBreadth = microbotBreadth
		self.spikeShape = spikeShape
		if (spikeShape == None):
			self.spikeShape = AbstractMicrobotBasicSpike.defaultSpikeShape
		
	
	def heuristic(self, freeNodePoint, angle):
		""" Computes the value of a freeNodePoint: a point in space that might be taken up by a Microbot.
		
		Lower values are prioritized. """
		
		# get the distance from the basePoint along the spikeDirection.
		
		## To compute easily, subtract by basePointPoint. This makes basePoint 0,0,0.
		freeNodePoint_basePoint = freeNodePoint.subtract(self.basePoint)
		
		## Now, dot them to get the first value.
		distAlongSpikeDirection = freeNodePoint_basePoint.getDot(self.spikeDirection)
		
		# get the distance from the freeNodePoint to the line formed through basePoint pointing to spikeDirection
		a_p = freeNodePoint.subtract(self.basePoint)
		a_pdn = a_p.getDot(self.spikeDirection)
		a_pdnxn = self.spikeDirection.multiply(a_pdn)
		a_p_a_pdnxn = a_p.subtract(a_pdnxn)
		distToLineThroughBasePoint = a_p_a_pdnxn.getMagnitude()
		
		# We can compute our heuristic value now.
		# If the value is lower, it means this point will be prioritized when setting a Microbot.
		
		return self.spikeShape(self, distToLineThroughBasePoint, angle, distAlongSpikeDirection)
	
	class BotThread:
		def __init__(self, spike, firstPoint, angle):
			self.bots = []
			self.spike = spike
			self.nextPoint = firstPoint
			self.angle = angle
			
		def heuristic(self):
			return self.spike.heuristic(self.nextPoint, self.angle)
			
		def append(self, microbot):
			""" When appending, the Microbot is posed. """
			
			self.bots.append(microbot)
			
			tailPoint = self.nextPoint.add(self.spike.spikeDirection.multiply(self.spike.microbotSpan))
			
			microbot.setPose(
				self.nextPoint,
				self.nextPoint.add(self.spike.spikeDirection.multiply(self.spike.microbotSpan/2)),
				tailPoint)
			
			self.nextPoint = tailPoint
			
			
	class BotPlacementLinkedList:
		class BotPlacementElement:
			def __init__(self, point, value=float("inf")):
				self.prev = None
				self.next = None
				self.point = point
				self.value = value
		
		def __init__(self):
			self.head = AbstractMicrobotBasicSpike.BotPlacementLinkedList.BotPlacementElement(None)
			self.tail = self.head
			
		def shift(self):
			if (self.head == self.tail):
				return None
			output = self.head.next
			self.head.next = output.next
			if (output == self.tail):
				self.tail = self.head
			else:
				self.head.next.prev = self.head
			return output
			
		def add(self, point, value=float("inf")):
			n = AbstractMicrobotBasicSpike.BotPlacementLinkedList.BotPlacementElement(point, value)
		
			rover = self.head.next
			while (rover != None and rover.value<=value):
				rover = rover.next
			if (rover == None):
				self.tail.next = n
				n.prev = self.tail
				self.tail = n
			else:
				n.next = rover
				n.prev = rover.prev
				rover.prev.next = n
				rover.prev = n
			return n
			
		
	
	def calculate(self, microbotLineup, microbotCount, microbotThreadCount):
		""" Takes a Microbot from a lineup, up to the number of Microbots specified.
		This builds the spike, made of up to a number of microbot threads.
		
		Returns a list of AbstractMicrobotOriginArmTip that was used by this method.
		"""
		
		# Process:
		## Imagine a disk whose normal vector is the spikeDirection.
		## Fill this disk with circles through which a microbotThread will go through.
		## From a point in the center of each of these circles, imagine a line with spikeDirection.
		## Through that line, find the point where it intersects with the ground (or wherever the thread will begin forming.)
		
		# Part 1.1: Make the disk.
		
		## Produce a vector perpendicular to the spikeDirection.
		diskSweepVector = self.spikeDirection.getCross(Point.Z)
		if (diskSweepVector.isZero()):
			diskSweepVector = Point.X
		diskSweepVector.normalize()
		
		# Part 1.2: Fill this disk with circles.
		microbotThreads = [AbstractMicrobotBasicSpike.BotThread(self, self.basePoint, 0)]
		
		microbotThreadOrbit = 0
		microbotThreadCapacity = 0
		microbotThreadCapacityMax = 0
		microbotBreadth = self.microbotBreadth
		microbotThreadRadians = 0
		pi2 = pi*2
		while (len(microbotThreads)<microbotThreadCount):
			if (microbotThreadCapacity == 0):
				microbotThreadOrbit += 1
				
				# Compute the largest number of circles that can fit at that point.
				# Get the circumference at that orbit, then divide by the diamter of a microbot.
				# microbotThreadRadians = 2*pi*microbotThreadOrbit #*microbotBreadth/microbotBreadth
				microbotThreadCapacityMax = floor(pi2*microbotThreadOrbit)
				microbotThreadCapacity = microbotThreadCapacityMax
			
			# rotate the diskSweepVector
			microbotThreadOrbitAngle = diskSweepVector.rotate(self.spikeDirection, pi2*microbotThreadCapacity/microbotThreadCapacityMax)
			
			# get the point at this angle.
			threadPoint = self.basePoint.add(microbotThreadOrbitAngle.multiply(microbotBreadth*microbotThreadOrbit))
			microbotThreads.append(AbstractMicrobotBasicSpike.BotThread(self, threadPoint, microbotThreadOrbitAngle))
			
			microbotThreadCapacity -= 1
			
		## Part 1.3: Find the point where a line through each circle's center and normal intersects with the ground.
		
		for i in microbotThreads:
			i.nextPoint = i.nextPoint.getPointIntersectionByLineToPlane(self.spikeDirection, Point.ZERO, Point.Z)
		
		# Part 2: Prepare to begin.
		
		## Part 2.1: Set up a priority lane.
		microbotPriority = AbstractMicrobotBasicSpike.BotPlacementLinkedList()
		for i in microbotThreads:
			microbotPriority.add(i, i.heuristic())
		
		## Part 2.2: Initialize the microbots usage.
		microbotCounter = 0
		microbotAccounting = []
		
		## Part 3: begin.
		while (microbotCounter<microbotCount):
			# Get the next microbot we can use.
			nextMicrobot = microbotLineup.getOneOriginArmTip()
			if (nextMicrobot == None):
				break
				
			# Get the next point we can use.
			nextThread = microbotPriority.shift().point
			
			# Add this microbot to that thread. It will be posed as it is added.
			nextThread.append(nextMicrobot)
			
			# Put this back in the priority. The append operation earlier has updated its value.
			microbotPriority.add(nextThread, nextThread.heuristic())
			
			# Increment things.
			microbotAccounting.append(nextMicrobot)
			microbotCounter += 1
			
		# By this point, all the Microbots used have been posed.
		# Return a list of those Microbots.
		return microbotAccounting
		
		