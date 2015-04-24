from math import pi, floor, pow, atan2, sqrt

class MicrobotSpikeParametrics:
	def __init__(self, fc, fr, ft):
		self.fc = fc
		self.fr = fr
		self.ft = ft
		
def fc(self, o):
	return floor(pi2*o)

def fr(self, o, c):
	return o
	
def ft(self, o, c):
	return pi2*c/floor(pi2*o)

MicrobotSpikeParametrics.CIRCLE = MicrobotSpikeParametrics(fc, fr, ft)

def fc(self, o):
	return o*8

def fr(self, o, c):
	q = o*2
	qi = (c+o)%q
	qs = qi-o
	return sqrt(qs*qs+o*o)
	
def ft(self, o, c):
	q = o*2
	qi = (c+o)%q
	qu = floor((c+o)/q)%4
	if (qu == 0):
		return atan2(qi-o, o)
	elif (qu == 1):
		return atan2(o, o-qi)
	elif (qu == 2):
		return atan2(o-qi, -o)
	elif (qu == 3):
		return atan2(-o, qi-o)
	return 0
	
MicrobotSpikeParametrics.SQUARE = MicrobotSpikeParametrics(fc, fr, ft)