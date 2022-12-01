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

showTime = 1

rLow = 0.2 # TODO change to match paper
rAvgLow = 0# minimum average radius for trial
rAvgHigh = 0# max average radius for trial
#add function to use these and throw out trials that dont fit

rHigh = 0.4 # TODO change to match paper

sphereList = []
spheresOut = []

def getX(angle, distance):
	return circleCenterX + ((cirlceRadius * distance) * math.cos(angle))


def getY(angle, distance):
	return circleCenterY + ((cirlceRadius * distance) * math.sin(angle))


def makeSpheres(count, distance, rL, rH):
	global sphereList
	placementAngle = [0, 45, 90, 135, 180, 225, 270, 315]
	
	for j in range(count):
		
		spheres = []
		
		for i in placementAngle:
			angle = random.randint(i - jitter, i + jitter)
			
			spheres.append([
			getX(math.radians(angle), distance / distance2),
			getY(math.radians(angle), distance / distance2), 
			distance, 
			random.uniform(rL, rH) 
			]) 
			
		sphereList.append(spheres)
	
	
def addSpheres(spheres):
	global spheresOut
	
	for s in spheres:
		sphereAdd = vizshape.addSphere(s[3] * (s[2] /distance2))
		sphereAdd.setPosition(s[0], s[1], s[2])
		spheresOut.append(sphereAdd)


def removeSpheres():
	global spheresOut
	
	for s in spheresOut:
		s.remove()
	spheresOut = []


def experiment():
	global SphereList
	print(len(sphereList))
	for i in range(len(sphereList) -1):
		print(i)
		yield addSpheres(sphereList[i])
		yield viztask.waitTime(1)
		yield removeSpheres()
		
	


makeSpheres(count, distance1, rLow, rHigh)
makeSpheres(count, distance2, rLow, rHigh)
makeSpheres(count, distance3, rLow, rHigh)
random.shuffle(sphereList)

print(sphereList)

print("before")
theExperiment = viztask.schedule(experiment())
