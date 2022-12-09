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


count = 50
distance1 = 4
distance2 = 6
distance3 = 8

cirlceRadius = 2 # TODO change to match paper
circleCenterX = 0
circleCenterY = 3
jitter = 5

trialShowPause = 1 #time to pause after showing the trial spheres
fixationShowPause = 0.5 #time the fixation point is on screen before spheres show

rLow = 0.2 # TODO change to match paper
rHigh = 0.4 # TODO change to match paper

rAvgLow = 0.25# minimum average radius for trial
rAvgHigh = 0.35# max average radius for trial


probeRadLow = 0.1
probeRadHigh = 0.3

sphereList = []
spheresOut = []

def showFixationPoint():
	global spheresOut
	
	box1 = vizshape.addBox(size=(0.5, 0.1, 0.1), color = viz.WHITE)
	box2 = vizshape.addBox(size=(0.1, 0.5, 0.1), color = viz.WHITE)
	box1.setPosition(0,3,6)
	box2.setPosition(0,3,6)
	spheresOut.append(box1)
	spheresOut.append(box2)
	

def getX(angle, distance):
	return circleCenterX + ((cirlceRadius * distance) * math.cos(angle))


def getY(angle, distance):
	return circleCenterY + ((cirlceRadius * distance) * math.sin(angle))


def makeSpheres(count, distance, rL, rH):
	global sphereList
	placementAngle = [0, 45, 90, 135, 180, 225, 270, 315]
	
	
	tempCount = 0
	while tempCount < count:
	
		spheres = []
		meanRadius = []
		
		for i in placementAngle:
			angle = random.randint(i - jitter, i + jitter)
			radius = random.uniform(rL, rH)
			
			spheres.append([
			getX(math.radians(angle), distance / distance2),
			getY(math.radians(angle), distance / distance2), 
			distance,
			radius
			]) 
			meanRadius.append(radius)
		
		if rAvgHigh > mean(meanRadius) > rAvgLow:
			sphereList.append(spheres)
			tempCount += 1
	
	
def addSpheres(spheres):
	global spheresOut
	
	for s in spheres:
		sphereAdd = vizshape.addSphere(s[3] * (s[2] / distance2))
		sphereAdd.setPosition(s[0], s[1], s[2])
		spheresOut.append(sphereAdd)


def removeSpheres():
	global spheresOut
	
	for s in spheresOut:
		s.remove()
	spheresOut = []
	


scale_factor = 1

# Define a function to increase the scaling factor
def increase_scale(sphere):
    global scale_factor
    scale_factor *= 1.05
    sphere.setScale([scale_factor, scale_factor, scale_factor])

# Define a function to decrease the scaling factor
def decrease_scale(sphere):
    global scale_factor
    scale_factor /= 1.05
    sphere.setScale([scale_factor, scale_factor, scale_factor])


		

def response():
	global spheresOut
	global scale_factor
	spheresOut = []
	
	probeRadius = random.uniform(probeRadLow, probeRadHigh)
	probe = vizshape.addSphere(probeRadius)
	probe.setPosition(0, 2, distance2) #TODO check distance spawning
	spheresOut.append(probe)
	
	# Set the initial scaling factor for the sphere
	scale_factor = 1.0
	
	#info = vizinfo.InfoPanel(
	#"Trigger left to make the sphere smaller, trigger right to make the sphere larger", 
	#title = "Match the sphere shown out front of you to the average size of the spheres you just saw", 
	#margin = (100, 100), 
	#align = viz.ALIGN_CENTER_BOTTOM) # TODO will have to adjust for vr headset

	
	viz.callback(viz.KEYDOWN_EVENT, onKeyDown)

	yield viztask.waitKeyDown(" ")
	print("done")
	viz.callback(viz.KEYDOWN_EVENT, None)


	#info.remove()
	
	probeResponse = [probeRadius, scale_factor]
	viztask.returnValue(probeResponse)
	
def onKeyDown(key):
	if key == viz.KEY_LEFT:
		decrease_scale(spheresOut[0])
	elif key == viz.KEY_RIGHT:
		increase_scale(spheresOut[0])
	else:
		pass
	

def experiment():
	global SphereList
	#print(len(sphereList))
	for i in range(len(sphereList) -1):
		print(i)
		yield showFixationPoint()
		yield viztask.waitTime(fixationShowPause)
		yield addSpheres(sphereList[i])
		yield viztask.waitTime(trialShowPause)
		yield removeSpheres()
		probe = yield response()
		print(probe)
		yield removeSpheres()
	

#where the experiment is run from
makeSpheres(count, distance1, rLow, rHigh)
makeSpheres(count, distance2, rLow, rHigh)
makeSpheres(count, distance3, rLow, rHigh)
random.shuffle(sphereList)

theExperiment = viztask.schedule(experiment())
