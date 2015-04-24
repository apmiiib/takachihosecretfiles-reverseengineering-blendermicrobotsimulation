class AbstractMicrobotLineup:
	def __init__(self, array=[]):
		self.array = array
		self.roverIndex = 0;
		
	def __len__(self):
		return len(self.array)
		
	def append(self, value):
		self.array.append(value)
		
	def getOneOriginArmTip(self):
		output = self.array[self.roverIndex];
		self.roverIndex += 1
		if (self.roverIndex == len(self.array)):
			self.roverIndex = 0
		return output