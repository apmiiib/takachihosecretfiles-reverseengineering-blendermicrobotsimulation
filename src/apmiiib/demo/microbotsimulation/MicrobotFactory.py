import bpy
import mathutils

class MicrobotFactory:
	armatureName = "Microbot"
	meshName = "Microbot-Base"

	def getMesh(count):
		try:
			index = str(count).rjust(3, "0");
			mesh = bpy.data.objects[MicrobotFactory.meshName+"."+index]
			return mesh
		except:
			return None
			
	def getArmature(count):
		try:
			index = str(count).rjust(3, "0");
			armature = bpy.data.objects[MicrobotFactory.armatureName+"."+index]
			return armature
		except:
			return None
	
	def link(index):
	
		## Remember the new stuff.
		mesh = bpy.data.objects[MicrobotFactory.meshName+"."+index]
		armature = bpy.data.objects[MicrobotFactory.armatureName+"."+index]
		
		mesh.hide = False
		mesh.select = False
		mesh.hide_render = False
		armature.hide = False
		armature.select = False
		armature.hide = True
		
		## Now, we have to (metaphorically) link the two together.
		mesh.parent = armature
		mesh.modifiers["Armature"].object = armature
		mesh.hide_select = True

	def deselectAll():
		bpy.ops.object.select_all(action='DESELECT')
		
	def create(count=0):
		# An adaptation of my hair spike duplication code from one of my projects.
		# It carries the same limitations as the original, which is as follows: 
		
		# Currently, this duplication code assumes there is an equal number of "Microbot.xxx" and "Microbot-Base.xxx"
		# Also, that each Microbot.xxx has a correctly indexed corresponding Microbot-Base.xxx
		# Things will go wrong otherwise.
		
		microbotArmature0 = bpy.data.objects[MicrobotFactory.armatureName]
		microbotMesh0 = bpy.data.objects[MicrobotFactory.meshName]
		
		# Some operations depend on the selected object.
		MicrobotFactory.deselectAll();
		
		index = ""

		# Find the next index.
		while True:
			try:
				index = str(count).rjust(3, "0");
				bpy.data.objects[MicrobotFactory.armatureName+"."+index];
				count += 1;
			except:
				break
		
		## Linked-Duplicate the base Microbot.
		 
		# Select the base Microbot.
		microbotMesh0.hide_select = False
		microbotMesh0.select = True
		
		# execute duplication.
		bpy.ops.object.duplicate_move_linked()
		microbotMesh0.select = False
		bpy.data.objects[MicrobotFactory.meshName+"."+index].select = False
		
		# deselect 
		MicrobotFactory.deselectAll();
		
		## Duplicate the Microbot armature
		
		# Select the Armature
		microbotArmature0.hide_select = False
		microbotArmature0.select = True
		
		# Duplicate.
		bpy.ops.object.duplicate_move()
		microbotArmature0.select = False
		bpy.data.objects[MicrobotFactory.armatureName+"."+index].select = False
		
		MicrobotFactory.link(index)
		
		MicrobotFactory.deselectAll();
		
		# The end.