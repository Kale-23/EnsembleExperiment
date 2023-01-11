import viz
import viztask
import vizact
import vizshape
import vizinfo
import os


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

# These adjust the number of trials of each distannce, and how far the spheres are shown on the z axis from zero
count = 50 # How many spheres trials to create at a certain distance
distance1 = 4 # Distance from zero of foreground trials
distance2 = 6 # Distance from zero of Middle trials
distance3 = 8 # Distance from zero of Background trials

# These adjust the parameters for the imaginary circumferencne the spheres are placed on
cirlceRadius = 2 # Radius of circumference
circleCenterX = 0 # where the center of the circumference will be placed on the x axis
circleCenterY = 3 # where the center of the circumference will be placed on the y axis
jitter = 5 # degrees the spheres can jitter from thier placement angle (ie with jitter = 5, the sphere at 0 degrees will be randomly placed between 355 degrees and 5 degrees)

# Pause times between events of experiment
trialShowPause = 1 #time to pause after showing the trial spheres
fixationShowPause = 0.5 #time the fixation point is on screen before spheres show

# Radius values for spheres
rLow = 0.2 # Lowest radius a sphere can randomly be given
rHigh = 0.4 # Highest radius a sphere can randomly be given
rAvgLow = 0.25 # minimum average radius for spheres in each trial, if below this value sphere values for trial will be deleted and new values will be generated
rAvgHigh = 0.35 # maximum average radius for spheres in each trial, if above this value, sphere values for trial will be deleted ad ew values will be generated

# probe parameters
probeRadLow = 0.25 # Lowest radius the probe can randomly be given
probeRadHigh = 0.35 # Highest radius the probe can randomly be given
scale_factor = 1 # factor by which the radius of the probe will be scaled by when shown.
valueToScaleBy = 1.05 # value by which the scale factor of the probe is increased/decreased by every time '' is called

# response parameters
decreaseScaleFactorInput = viz.KEY_LEFT # participant input (keyboard/ joystick/ etc) that will multiply 'scale_factor' by 'valueToScaleBy'
increaseScaleFactorInput = viz.KEY_RIGHT # participant input (keyboard/ joystick/ etc) that will divide 'scale_factor' by 'valueToScaleBy'particip
endResponseInput = ' ' # participant input that confirms their probe size and ends response portion of trial.

# global lists
sphereList = [] # All spheres and trials are pregenerated before running the experiment, each trial is stored in this list. The trials stored will be lists of 8 sphere parameters per trial.
spheresOut = [] # Will hold any sphere entity that is currently being shown in the environment, is emptied anytime removeSpheres is called
trialProbeResponse = [] # holds the data of participant probe sphere responses for each trial (probeRadius, probeResponseTime).

'''
Creates the '+' mark within the middle of the imaginary circumference. 
The fixation point will be shown at the same distance as the spheres, and will scale with distance so as to always appear to be same size.
'''
def showFixationPoint(dist):
	global spheresOut
	
	box1 = vizshape.addBox(size=(0.5, 0.1, 0.1), color = viz.WHITE)
	box2 = vizshape.addBox(size=(0.1, 0.5, 0.1), color = viz.WHITE)
	box1.setPosition(0,3,dist)
	box1.setScale([dist / distance2, dist / distance2, dist / distance2])
	box2.setPosition(0,3,dist)
	box2.setScale([dist / distance2, dist / distance2, dist / distance2])
	spheresOut.append(box1)
	spheresOut.append(box2)
	

'''
Helper method for makeSpheres that finds the x value within the imaginary circumference to place the sphere at. 
'''
def getX(angle, distance):
	return circleCenterX + ((cirlceRadius * distance) * math.cos(angle))

'''
Helper method for makeSpheres that finds the y value within the imaginary circumferecne to place the sphere at. 
'''
def getY(angle, distance):
	return circleCenterY + ((cirlceRadius * distance) * math.sin(angle))

'''
Creates 8 spheres for each trial, for 'count' number of trials. 
Sphere parameters will be gennerated every 45 degrees (+/- 'jitter') around the imaginary circumference starting at 0 degrees up to 315 degrees. 
The imaginary circumference will always appear to be the same size no matter the distance from the participant.
x parameter generated from getX(), y parameter generated from getY(), distance is z value from z = 0 given by 'distance', radius is randomly generated between 'rLow' and 'rHigh'.
If the average radius of all 8 spheres is between 'rAvgLow' and 'rAvgHigh', the trial is accepted and added to 'sphereList', else it is thrown out and new parameters are chosen.
'''
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
	

'''
takes a list of sphere parameters, adds them to the environment, and adds them to 'spheresOut'.
'''
def addSpheres(spheres):
	global spheresOut
	
	for s in spheres:
		sphereAdd = vizshape.addSphere(s[3] * (s[2] / distance2))
		sphereAdd.setPosition(s[0], s[1], s[2])
		spheresOut.append(sphereAdd)

'''
removes any sphere entities within 'spheresOut' from the environement, and empties 'spheresOut'.
'''
def removeSpheres():
	global spheresOut
	
	for s in spheresOut:
		s.remove()
	spheresOut = []
	
'''
helper method for onKeyDown().
every time it is called, will multiply 'scale_factor' by 'valueToScaleBy' for individual trial.
'''
def increase_scale(sphere):
    global scale_factor
    scale_factor *= valueToScaleBy
    sphere.setScale([scale_factor, scale_factor, scale_factor])

'''
helper method for onKeyDownn().
every time it is called, will divide 'scale_factor' by 'valueToScaleBy' for individual trial.
'''
def decrease_scale(sphere):
    global scale_factor
    scale_factor /= valueToScaleBy
    sphere.setScale([scale_factor, scale_factor, scale_factor])

'''
helper method for response().
when called, if 'decreaseScaleFactorInput' is input, will call decrease_scale(),
if 'increaseScaleFactorInput' is input, will call increase_scale(),
and will do nothing if any other button is pressed
'''
def onKeyDown(key):
	if key == decreaseScaleFactorInput:
		decrease_scale(spheresOut[0])
	elif key == increaseScaleFactorInput:
		increase_scale(spheresOut[0])
	else:
		pass

'''
creates probe sphere parameters and puts the probe into the enviromet and into 'spheresOut'. 
The probe's radius is random between 'probeRadLow' and 'probeRadHigh', the distance is the same as the trial's that was just shown, and is always x = 0, y = 2.
Once the probe is shown, participant is allowed input (from keyboard/ joystick/ etc). Will call onKeyDown() on any input.
If 'endResponseInput' is input, the participant can no longer provide input until the next trial, and the current probe's initial radius and scale factor are returned.
'''
def response(dist):
	global spheresOut
	global scale_factor
	spheresOut = []
	
	# Probe setupt and output to environment
	probeRadius = random.uniform(probeRadLow, probeRadHigh)
	probe = vizshape.addSphere(probeRadius)
	probe.setPosition(0, 2, dist)
	spheresOut.append(probe)
	
	# Set the initial scaling factor for the probe in this trial
	scale_factor = 1.0

	# Allows participant input during this time until 'endResponseInput' is input.
	viz.callback(viz.KEYDOWN_EVENT, onKeyDown)
	yield viztask.waitKeyDown(endResponseInput)
	
	# makes it so participant cannot change 'scale_factor' outside of response time.
	viz.callback(viz.KEYDOWN_EVENT, None)
	
	#probeResponse = [probeRadius, scale_factor]
	viztask.returnValue([probeRadius, scale_factor, probeRadius * scale_factor])
	

	
'''
for each trial in 'sphereList:
The fixation point will be shown for 'fixationShowPause' seconds.
The spheres of the trial will show for 'trialShowPause' seconds.
Both the fixation point and spheres will be taken off the screen, and the probe will appear.
The participant is allowed to adjust the size of the probe until they are satisfied, and then the probe is taken off the screen.
'''
def experiment():
	global SphereList
	#print(len(sphereList)) for testing purposes
	global trialProbeResponse
	
	# runs through all trials stored in 'sphereList'
	for i in range(len(sphereList)):
		#print(i)
		yield showFixationPoint(sphereList[i][0][2])
		yield viztask.waitTime(fixationShowPause)
		yield addSpheres(sphereList[i])
		yield viztask.waitTime(trialShowPause)
		yield removeSpheres()
		
		startTime = viz.tick()
		probe = yield response(sphereList[i][0][2])
		responseTime = viz.tick() - startTime
		resp = [probe, responseTime]
		trialProbeResponse.append(resp)
		
		yield removeSpheres()
	writeOut()
	print("experiment over")

'''
helper for writeOut. automatically gets and updates the current participant number for naming output file.
'''
def getParticipantNumber():
	if not os.path.exists('currentParticipant.txt'):
		with open('currentParticipant.txt','w') as f:
			f.write('1')
	with open('currentParticipant.txt','r') as f:
		st = int(f.read())
		out = st
		st+=1 
	with open('currentParticipant.txt','w') as f:
		f.write(str(st))
	
	return out

'''
Creates new file and records trial, sphereNumber, sphereX, sphereY, sphereDist, sphereRadius, probeAnswerRadius, probeAnswerTime for each sphere within a trial, for each trial.
'''
def writeOut():
	
	path = "participantData"
	participantNumber = getParticipantNumber()
	
	if not os.path.exists(path):
		os.makedirs(path)

	filename = "Participant" + str(participantNumber) + ".csv"
	with open(os.path.join(path, filename), 'w') as outfile:
		try:
			outfile.write("trial,sphereNumber,sphereX,sphereY,sphereDist,sphereRadius,probeStartingRadius,probeFinalScaleFactor,probeAnswerRadius,probeResponseTime\n")
			
			for i in range(len(sphereList)):
				for j in range(len(sphereList[i])):
					print(trialProbeResponse[i])
					outfile.write("{},{},{},{},{},{},{},{},{},{}\n".format(i + 1, j + 1, sphereList[i][j][0], sphereList[i][j][1], sphereList[i][j][2], sphereList[i][j][3], trialProbeResponse[i][0][0],trialProbeResponse[i][0][1],trialProbeResponse[i][0][2],trialProbeResponse[i][1]))
			#outfile.close()
			
		except IOError:
			viz.logWarn("Dont have the file permissions to log data")


#where the experiment is run from
#makeSpheres(count, distance1, rLow, rHigh)
#makeSpheres(count, distance2, rLow, rHigh)
#makeSpheres(count, distance3, rLow, rHigh)
makeSpheres(2, distance2, rLow, rHigh) # testing purposes only, uncomment above and delete once testing is over
random.shuffle(sphereList)

theExperiment = viztask.schedule(experiment())
