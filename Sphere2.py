import viz
import viztask
import vizact
import vizshape
import vizinfo

import random
import math
from statistics import mean

#setup
viz.setMultiSample(4)
viz.fov(60)
viz.go()
viz.MainView.setPosition(0, 3, 0)

#grey grid on floor TODO remove after testing
grid = vizshape.addGrid()
grid.color(viz.GRAY)

'''
#x,y,z world axis TODO remove after testing
world_axes = vizshape.addAxes()
X = viz.addText3D('X',pos=[1.1,0,0],color=viz.RED,scale=[0.3,0.3,0.3],parent=world_axes)
Y = viz.addText3D('Y',pos=[0,1.1,0],color=viz.GREEN,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)
Z = viz.addText3D('Z',pos=[0,0,1.1],color=viz.BLUE,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)
'''

#Add the ground plane TODO prob switch this in final experiment
#ground = viz.addChild('sky_day.osgb')




#sphere circle spawning parameters
cirlceRadius = 2 # TODO change to match paper
circleCenterX = 0
circleCenterY = 3
distanceZ = 10 #distance from (0,0, 0) in the z direction to spawn the spheres
jitter = 10



#sphere parameters
rLow = 0.3 # TODO change to match paper
rHigh = 0.1 # TODO change to match paper
testRadLow = 0.1
testRadHigh = 0.3
showTime = 1
numberTrials = 10


spheresOut = []
spheres = []

def getX(angle):
	return circleCenterX + (cirlceRadius * math.cos(angle))

def getY(angle):
	return circleCenterY + (cirlceRadius * math.sin(angle))

def showSpheres(distance, rL, rH):
	global spheresOut
	global spheres
	placementAngle = [0, 45, 90, 135, 180, 225, 270, 315]
	spheres = []
	
	for i in placementAngle:
		angle = random.randint(i - jitter, i + jitter)
		
		spheres.append([
		getX(math.radians(angle)), 
		getY(math.radians(angle)), 
		distance, 
		random.uniform(rL, rH)
		]) 
	
	for i in spheres:
		sphereAdd = vizshape.addSphere(i[3])
		sphereAdd.setPosition(i[0], i[1], i[2])
		spheresOut.append(sphereAdd)
	

def removeSpheres():
	for s in spheresOut:
		s.remove()

def testingSphere(distance):
	global spheresOut
	spheresOut = []
	
	testAdd = vizshape.addSphere(random.uniform(testRadLow, testRadHigh))
	testAdd.setPosition(0, 1, distance) #TODO check distance spawning
	spheresOut.append(testAdd)
		

def response():
	info = vizinfo.InfoPanel(
	"Trigger left to make the sphere smaller, trigger right to make the sphere larger", 
	title = "Match the sphere shown out front of you to the average size of the spheres you just saw", 
	margin = (100, 100), 
	align = viz.ALIGN_CENTER_BOTTOM
	) # TODO will have to adjust for vr headset
	yield viztask.waitTime(5) # TODO remove after testing
	answer = 1 # TODO remove after testing
	info.remove()
	viztask.returnValue(answer)
	
def experiment():
	for i in range(numberTrials):
		yield showSpheres(5, rLow, rHigh)
		print(spheres)
		yield viztask.waitTime(showTime)
		yield removeSpheres()
		yield testingSphere(6)
		yield response()
		yield removeSpheres()
		


#run the experiment
myTask = viztask.schedule(experiment())

