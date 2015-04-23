from math import *
from mathutils import *

class Point:
	def __init__(self, x=0, y=0 , z=0):
		self.x = x
		self.y = y
		self.z = z
		
		self.isUnitVector = False;
		
	def set(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z
		self.isUnitVector = False
		return self

	def setPoint(self, p2):
		self.x = p2.x
		self.y = p2.y
		self.z = p2.z
		self.isUnitVector = False
		return self

	def getDist(self, p2):
		x = self.x-p2.x
		y = self.y-p2.y
		z = self.z-p2.z
		return sqrt(x*x+y*y+z*z)
		
	def getDist2(self, p2):
		x = self.x-p2.x
		y = self.y-p2.y
		z = self.z-p2.z
		return x*x+y*y+z*z

	def getUnitVectorTo(self, p2=None):
		dist = self.getDist(p2)
		if (dist>0):
			x = p2.x-self.x
			y = p2.y-self.y
			z = p2.z-self.z
			return Point(x/dist, y/dist, z/dist).setIsUnitVector()
		else:
			return Point(0, 0, 0)

	def setDistFrom(self, p2, dist):
		"""Moves this point so the distance from this point to another point is as specified.
			Preserves their relative angle.
			That is to say, any position translation will be along the line drawn by self and p2.
		"""

		dist0 = getDist(p2)
		self.x = p2.x-(p2.x-self.x)/dist0*dist
		self.y = p2.y-(p2.y-self.y)/dist0*dist
		self.z = p2.z-(p2.z-self.z)/dist0*dist
		self.isUnitVector = False
		
	def setIsUnitVector(self, value=True):
		self.isUnitVector = value
		return self

	def increase(self, p2):
		"""Increase modifies the Point's coordinates.
		"""
		self.x += p2.x
		self.y += p2.y
		self.z += p2.z
		self.isUnitVector = False
		return self
		
	def add(self, p2):
		"""Also works like increase() but a new Point is generated instead of modifying this one.
		"""
		return Point().setPoint(self).increase(p2)
		
	def decrease(self, p2):
		"""Decrease modifies the Point's coordinates.
		"""
		self.x -= p2.x
		self.y -= p2.y
		self.z -= p2.z
		self.isUnitVector = False
		return self
		
	def scale(self, n, o=None, p=None):
		"""Multiplies the coordinate values.
		"""
		if (o == None):
			o = n
		if (p == None):
			p = n
		self.x *= n
		self.y *= o
		self.z *= p
		self.isUnitVector = False
		return self
	
	def multiply(self, n, o=None, p=None):
		"""Also works like scale() but a new Point is generated instead of modifying this one.
		"""
		return Point().setPoint(self).scale(n, o, p)
	
	def negate(self):
		return Point().set(-self.x, -self.y, -self.z)
	
	def subtract(self, p2):
		"""Also works like decrease() but a new Point is generated instead of modifying this one.
		"""
		return Point().setPoint(self).decrease(p2)
		
	def turn(self, axis, angle):
		cost = cos(angle)
		sint = sin(angle)
		_cost = 1-cost
		
		axis = axis.getDirection()
		x = axis.x
		y = axis.y
		z = axis.z
		
		"""
		R11 = x*x*_cost+cost
		R21 = y*x*_cost+z*sint
		R31 = z*x*_cost-y*sint
		R12 = x*y*_cost-z*sint
		R22 = y*y*_cost+cost
		R32 = z*y*_cost+x*sint
		R13 = x*z*_cost+y*sint
		R23 = y*z*_cost-x*sint
		R33 = z*z*_cost+cost
		"""
		
		xy = x*y
		xz = x*z
		yz = y*z
		
		xy_cost = xy*_cost
		xz_cost = xz*_cost
		yz_cost = yz*_cost
		
		xsint = x*sint
		ysint = y*sint
		zsint = z*sint
		
		R11 = x*x*_cost+cost
		R21 = xy_cost+zsint
		R31 = xz_cost-ysint
		R12 = xy_cost-zsint
		R22 = y*y*_cost+cost
		R32 = yz_cost+xsint
		R13 = xz_cost+ysint
		R23 = yz_cost-xsint
		R33 = z*z*_cost+cost
		
		xn = self.x*R11+self.y*R21+self.z*R31
		yn = self.x*R12+self.y*R22+self.z*R32
		zn = self.x*R13+self.y*R23+self.z*R33
		
		self.x = xn
		self.y = yn
		self.z = zn
		
		return self
	
	def rotate(self, axis, angle):
		return Point().setPoint(self).turn(axis, angle)
		
	def normalize(self):
		dist = self.getMagnitude()
		if (dist>0):
			self.x = self.x/dist
			self.y = self.y/dist
			self.z = self.z/dist
			self.isUnitVector = True
		return self
		
	def getDot(self, p2):
		return self.x*p2.x+self.y*p2.y+self.z*p2.z
		
	def getCross(self, p2):
		return Point(self.y*p2.z-self.z*p2.y, self.z*p2.x-self.x*p2.z, self.x*p2.y-self.y*p2.x)
	
	def getMagnitude(self):
		return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
		
	def getMagnitude2(self):
		return self.x*self.x+self.y*self.y+self.z*self.z
		
	def getDirection(self):
		if (self.isUnitVector):
			return self.clone()
		else:
			return Point.getUnitVectorTo(Point.ZERO, self)
	
	def getPointIntersectionByLineToPlane(self, lineDirection, planePoint, planeNormal):
		lineDirection = lineDirection.getDirection()
		planeNormal = planeNormal.getDirection()
		
		# if a line is p = dl + l0 and a plane is (p - p0).n = 0
		# then a plane-line intersection is d = (p0 - l0).n / l.n
		# a single-point intersection exists if the denominator is not zero.
		ldn = lineDirection.getDot(planeNormal)
		if (ldn == 0.0):
			return None
		p0_l0dn = planePoint.subtract(self).getDot(planeNormal)
		d = p0_l0dn/ldn
		
		return lineDirection.multiply(d).add(self)
		
	
	def toVector(self):
		return Vector((self.x, self.y, self.z))
		
	def toTuple(self):
		return (self.x, self.y, self.z)
		
	def toTuple4(self):
		return (self.x, self.y, self.z, 0)
		
	def toBoneRotationMatrix4(self):
		""" The direction vector produced by the model actually does not have enough information to produce a complete rotation matrix;
			it lacks rotation information for one axis.
			
			We will therefore supply the missing information ourselves.
			Assume that there won't be any rotation along the Y-axis.
			If the vector is pointing straight up, we'll assume the Y-axis is along Y+.
			
			If more information is needed, it can be passed as another paramater to this function.
		"""
		
		""" There appears to be a curious quirk with Blender 2.69, 
		where an Identity Matrix is treated as having a +90-degree rotation along the Z-axis.
		We'll premultiply our output matrix with a -90-degree rotation to compensate.
		
		UPDATE: This quirk is because a Blender bone points at Y+ if its matrix is an identity matrix,
			regardless of its original orientation.
		"""
		
		""" Produce our basis vectors. """
		y = self.getDirection()
		x = y.getCross(Point.Z);
		if (x.isZero()):
			x = Point.X
		else:
			x = x.normalize()
		z = x.getCross(y)
		
		return Matrix(((x.x, y.x, z.x, 0),
						(x.y, y.y, z.y, 0),
						(x.z, y.z, z.z, 0),
						(0, 0, 0, 1)))
		
	def matrixMultiply4x4(a, b):
		o = Matrix()
		for i in range(0, 4):
			for j in range(0, 4):
				o[i][j] = a[i][0]*b[0][j]+a[i][1]*b[1][j]+a[i][2]*b[2][j]+a[i][3]*b[3][j]
		return o
	
	def isZero(self):
		return (self.x == 0.0) and (self.y == 0.0) and (self.z == 0.0)
		
	def clone(self):
		return Point(self.x, self.y, self.z)
		
	ZERO = None
	X = None
	Y = None
	Z = None
	T4 = (0, 0, 0, 1)
	
Point.ZERO = Point(0, 0, 0)
Point.X = Point(1, 0, 0)
Point.Y = Point(0, 1, 0)
Point.Z = Point(0, 0, 1)
