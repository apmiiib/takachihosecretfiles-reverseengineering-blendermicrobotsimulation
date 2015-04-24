from apmiiib.abstract.geom.Point import Point
from mathutils import Vector

class ActorMicrobotOriginArmTip:
	"""This class uses info from the AbstractMicrobotOriginArmTip object and applies it to a physical representation of a microbot.
	This implementation expects the input armature to have these bones:
	
		--> Arm_L-Center - the bone which controls the left arm and center. Origin point.
			+-> Arm_R - child bone; the bone which controls the right arm.
			
		The bones are expected to have XZY Euler as rotation config.
	"""
	
	def __init__(self, data, armature):
		self.data = data
		self.data.being = self
		self.armature = armature
		
		self.bone1 = armature.pose.bones["Arm_L-Center"]
		self.bone2 = armature.pose.bones["Arm_R"]
		self.bone1mat = None
		
		self.update()
		
	def update(self):
		scale = self.data.span/10.55;
		self.armature.scale = Vector((scale, scale, scale));
		
		self.armature.location = self.data.o.toVector()
		
		m1v = self.data.getUnitVectorOC()
		
		# Compute the matrix for bone1.
		m1 = m1v.toBoneRotationMatrix4()
		
		# Commit bone1.
		self.mat1UV = m1
		m1p = self.bone1.matrix.copy()
		self.bone1.matrix = m1.copy()
		
		# Compute the matrix for bone2.
		# Get original-basis vector for the next bone.
		m2g = self.data.getUnitVectorCT().toBoneRotationMatrix4()
		
		# Use this to cancel off rotation by bone1
		m1t = m1.copy()
		m1t.transpose()
		m1p[0][3] = 0
		m1p[1][3] = 0
		m1p[2][3] = 0
		# m1p.transpose()
		
		m2 = Point.matrixMultiply4x4(Point.matrixMultiply4x4(m2g, m1t), m1p)
		
		# Set the position.
		m2[0][3] = m1v.x*5.275
		m2[1][3] = m1v.y*5.275
		m2[2][3] = m1v.z*5.275
		
		# Commit
		self.mat2UV = m2
		self.bone2.matrix = m2
		
		return self
		
		