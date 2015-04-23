I was able to generate a spike with the code here, but it requires that a lot of conditions be met because of present code limitations (and a lack of imagination from my part.):

- There must be an armature named "Microbot" and a child mesh "Microbot-Base". There also must be a copy of each with ".000" at the end. However, they may all be hidden and not rendered. These are the Source Copies.
- The armature must have a root bone "Arm_L-Center" which has a child bone "Arm_R". The first's tail is the second's head, and are found at the very center of the armature. Both bones have equal length and have a 0-degree roll.
- The armature (and therefore the mesh) must originally be pointing at the Y+ direction; the left arm's tip must be at the armature's origin, and the left-to-right-arm direction is the Y+ direction.
- The Source Copies must not be posed; they must have 0-degree rotations in all axes.
- KNOWN BUG: Recalculating a spike requires that the entire Blender software be restarted; the reshapeSpike function -- or rather, the underlying code that poses the armatures, which is used by this function -- is bugged. The armature pose code only works the first time it is used on an object.
- You must run (by importing) apmiiib/demo/microbotsimulation/SpikeDemonstration.py to generate a spike; you have to edit the file itself to set the parameters for creating that spike.
- The spike grows from the ground at Z=0. Therefore, the spike's angle cannot be parallel to the ground.
- (Probably more, but I can't think of another one anymore as of writing.)

Run the script on the Microbot Base demo. The parameters are as follows (edited in the script file):

	microbotLimit - the number of microbots to use.
	microbotThreads - max number of lines of microbots that a spike will be made of.
	radiusHeightRatio - defines the radius of the spike relative to its height. meaningless on its own if you define your own spike shape function
	spikeDirection - the direction vector that the spike will point at. This does NOT represent the point in space that the spike will point at.
	spikeBasePoint - where the spike's center is guaranteed to pass through. The spike begins from the ground at Z=0, then grows through this point, at an angle specified to spikeDirection.
	microbotSpan  - the length of the microbot.
	microbotBreadth - the diameter of the microbot.
	
	spikeShape - a function that you can redefine; it takes three parameters: polar R, polar angle T, and Z. its return value defines how the spike will be shaped.
		Example: a straight conical spike of microbots is defined by
			y = R+cT
		where c is how sharp the cone is (the smaller, the sharper)
	

# Takachiho Secret Files - Reverse Engineering - Microbot Simulation for Blender

[ Takachiho Hiro : Journal ] During my investigation of the space-time dimensional disturbances, and my subsequent arrival on the dimension responsible, I have discovered my parallel counterpart in the city near the place where some portal experimentation was carried out that caused the disturbances. In this apparent mix of America's San Francisco and my homeland's Tokyo and Shibuya, I have found one "Hiro Hamada", who forms part of his own Big Hero 6.

I came across one of his very interesting inventions: the Microbot. From all footage I've discovered, I learned that he showcased his invention in a university exhibit in their instiute of technology, then was subsequently stolen by one of the professors in that institution, in a bid for revenge over the then-apparent loss of his daughter to the aforementioned portal experimentation. Looking at their operation, I am intrigued in the applicability and the potential utility of these Microbots.

It would be dangerous to take this technology back to my home dimension. Nevertheless, in the interest of study, I have studied every footage available of the Microbots I seek to replicate, lacking access to a sample of the actual technology. I have not yet communicated with Hamada Hiro about this -- if it were me, I would get hold of one of his devices, or the blueprints to make them -- and given the role his Microbots played during the course of its existence, I am uncertain of the proper and appropriate time to ask him, or whether I should even do so.

Truth be told, I marvel at the technology level in this dimension. Certainly, those who deal with them would be much more advanced than anyone in my homeworld. I would feel embarrassed if I am to take one of them with me back to my home (for a visit/tour, of course), only to show how backwards our own technology levels are in comparison. I mused that even the most ordinary tinker here would be more knowledgable and advanced than the most innovative researchers and scientists at home. And then, I don't know if it's possible to replicate advanced technology here back home.

To say nothing of my counterpart, Hamada Hiro. (Well, I'll say it anyway.) Even by the standards of this world, he seems to be far more advanced than anyone else. Local online archives indicate that he (and his deceased brother)'s something of a robotics prodigy, with at one point being able to prove a mathematics theorem at a young age where mathematicians of his day had extreme difficulty resolving.

My investigation requires me that I go as silently as possible and avoid being noticed; thus, I can only watch them from the shadows. (My handy Ghost Cloak prevents my detection, but I'm not sure if it would work with technology here.) However, I will seize the first opportunity to contact them in person. I am keenly interested in meeting the local Big Hero 6 and learn more of the nature of their team, and I look forward to that possibility. Until then, I will at least make sure that no harm comes to then unawares, as I monitor them from the dark.

Well, enough about that. I'm here to attempt to produce a formulation that describes the behavior of Hamada Hiro's Microbots as they form shapes, and simulate it in a visualization software. Given that I have a bit of trouble coming up with a suitable implementation, I must say this Hiro here could very well trump my own intelligence. Again, I look forward to interacting with him and maybe share some technologies and stories.

[ ooc ] Files here are meant to be used for Blender 2.69. It comes in two parts: abstract implementation -- where the Microbot's behavior are mathematically computed -- and Blender interfacing, where all that math is converted into graphics by setting the necessary x, y, z, and rotation coordinates. I don't know if I can make a generalization of the Microbot's behavior to form all shapes and transitions, or if there even is one -- for all I know, the Disney animators probably used different piecewise functions for different cases. I will therefore just implement one behavior to achieve one effect -- namely, spikes of Microbots appearing from the ground, as seen in Hiro Hamada's gameplay demo in Disney Infinity -- until I notice a possible general solution.
