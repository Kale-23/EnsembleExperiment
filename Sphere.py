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

#x,y,z world axis TODO remove after testing
world_axes = vizshape.addAxes()
X = viz.addText3D('X',pos=[1.1,0,0],color=viz.RED,scale=[0.3,0.3,0.3],parent=world_axes)
Y = viz.addText3D('Y',pos=[0,1.1,0],color=viz.GREEN,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)
Z = viz.addText3D('Z',pos=[0,0,1.1],color=viz.BLUE,scale=[0.3,0.3,0.3],align=viz.ALIGN_CENTER_BASE,parent=world_axes)

#Add the ground plane TODO prob switch this in final experiment
ground = viz.addChild('sky_day.osgb')


# IMPORTANT #

participant = 1

#sphere parameters
rMean = 0.5 #mean of radius of spawned spheres (in meters) mean will differ slightly from this number in each trial
rSTD = 0.25 #standard deviation of the radius of spawned spheres (in meters)
sphereCount = 10 #how many spheres to spawn in each trial
trialCount = 10 #how many trials to complete
sphereShowTime = 1 #seconds to show sphere before disappearing

#where spheres will show up
leftX = -5 #left bounding wall for spawned spheres
rightX = 5 #right bounding wall for spawned spheres
bottomY = 1 #bottom bounding wall for spawned spheres
topY = 5 #top bounding wall for spawned spheres
distance = 10 #distance from (0,0, 0) in the z direction to spawn the spheres

#globals
step = 0.1 #percent of test sphere radius to change between trials
prevTestSphere = 0 #controls stepwise determination of testing sphere
spheres = [] #will contain all sphere parameters stored in individual dictionaries
spheresInEnv = [] #will contain sphere objects that are currently being showed to participant
experiment = [] #containns all data gathered from the experiment

'''
creates (sphereCount) sphere parameters
* spheres will not overlap when created
* outputs parameters to spheres list
'''
def makeSpheres():
	global spheres
	spheres = []
	while len(spheres) < sphereCount:

		sphere = {
		'x': random.uniform(leftX, rightX),
		'y': random.uniform(bottomY,topY),
		'r': random.gauss(rMean, rSTD),
		}
		
		overlap = False
		for num2 in range(len(spheres)):
			test = spheres[num2]
			d = math.dist([test.get('x'), test.get('y')], [sphere.get('x'), sphere.get('y')])
			if d < (test.get('r') + sphere.get('r')):
				#it intersects
				overlap = True
				break
				
		if overlap == False:
			spheres.append(sphere)
			
'''
adds spheres in spheres list to environment
* adds the created sphere objects to spheresInEnv list
'''
def addSpheres():
	global spheresInEnv
	spheresInEnv = []
	for s in spheres:
		sphereAdd = vizshape.addSphere(s.get('r'))
		sphereAdd.setPosition(s.get('x'), s.get('y'), distance)
		spheresInEnv.append(sphereAdd)
		
'''
removes spheres from environment
'''
def removeSpheres():
	for s in spheresInEnv:
		s.remove()
		
'''
gets the average radius of current trial's spheres.
spawns a test sphere with a radius(prevTestSphere) percent
larger/smaller of the average radius.
'''
def testingSphere(rad):
	global spheresInEnv
	global prevTestSphere
	spheresInEnv = []
	adjustedRad = rad * (1 + prevTestSphere)
	
	testAdd = vizshape.addSphere(adjustedRad)
	testAdd.setPosition(0, 1, distance) #TODO check distance spawning
	spheresInEnv.append(testAdd)
		
'''
Determines whether to step up or down the percent over/under the average sphere radius
for the test sphere in each trial
'''
def stepwiseCalc(response):
	global prevTestSphere
	global step
	if response == "Larger":
		prevTestSphere = prevTestSphere + step
	if response == "Smaller":
		prevTestSphere = prevTestSphere - step

'''
Sets up info panel, gets response, and returns smaller/larger guess
'''
def response():
	info = vizinfo.InfoPanel("Is the sphere larger or smaller", title = "Please select an answer", margin = (100, 100), align = viz.ALIGN_CENTER_BOTTOM) #will have to adjust for vr headset
	
	info.addSeparator()
	smaller = info.addLabelItem('Smaller', viz.addRadioButton('size'))
	larger = info.addLabelItem('Larger', viz.addRadioButton('size'))
	
	info.addSeparator()
	
	submitButton = info.addItem(viz.addButtonLabel('Submit'),align=viz.ALIGN_RIGHT_CENTER)
	
	''' TODO maybe figure this out
	#make sure at least smaller or larger is pressed
	answered = False
	if (smaller.get() == viz.DOWN) or (larger.get() == viz.DOWN):
		answered = True
	'''
	
	#if submit is pressed, return answer and remove info panel
	yield viztask.waitButtonUp(submitButton)
	if smaller.get() == viz.DOWN:
		info.remove()
		answer = "Smaller"
	elif larger.get() == viz.DOWN:
		info.remove()
		answer = "Larger"
	else:
		info.remove()
		answer = "NA"
	viztask.returnValue(answer)
	

'''
returns average of spheres
'''
def getAverageRadius():
	tempList = []
	for s in spheres:
		tempList.append(s.get('r'))
	return mean(tempList)

'''
excecutes and records results to outfiles
'''
def executeExperiment():
	global experiment
	global prevTestSphere
	experiment = []
	
	#repeats for number of trials
	for trialNumber in range(trialCount):
		#makes the spehers, adds the spheres, waits the sphereShowTime length, then removes spheres
		yield makeSpheres()
		sphereParams = spheres
		rad = getAverageRadius()
		yield addSpheres()
		yield viztask.waitTime(sphereShowTime)
		yield removeSpheres()
		
		#adds the testingSphere, shows info panel to chose smaller/larger, calculates next step up/down, removes the test sphere
		yield testingSphere(rad)
		testRad = rad * (1 + prevTestSphere)
		resp = yield response()
		currStep = prevTestSphere
		yield stepwiseCalc(resp)
		yield removeSpheres()
		
		#records all data from above into trial dictionary
		trial = {
		'trialNumber': trialNumber + 1, #done
		'spheres': sphereParams, #done
		'averageRadius': rad, #done
		'testSphereRadius': testRad, #done
		'step': currStep, #done
		'guess': resp #done
		}
		
		#appends the trial dictionary in overall list of trials
		experiment.append(trial)
		print("trial done: ", trialNumber + 1)
	#writes data to outfile
	writeOut()
	print("done all")




'''
Writes files out for the experiment
* One file contains trial#, average radius of trial, and the participant guess
* One file for sphere parameters
'''
def writeOut():
	try:
		outfile = open("Paricipant" + str(participant) + ".csv", "w")
		outfile.write("trial,actualRadius,testRadius,step,guess\n")
		
		for trial in experiment:
			outfile.write("{},{},{},{},{}\n".format(trial.get('trialNumber'), trial.get('averageRadius'), trial.get('testSphereRadius'), trial.get('step'), trial.get('guess')))
		outfile.close()
		
		outfile2 = open("Paricipant" + str(participant) + "Spheres" + ".csv", "w")
		outfile2.write("trial,sphereX,sphereY,sphereR\n")
		
		for trial in experiment:
			tri = str(trial.get('trialNumber'))
			for i in range(len(trial.get('spheres'))):
				outfile2.write(tri + "," + str(trial.get('spheres')[i].get('x')) + "," + str(trial.get('spheres')[i].get('y')) + "," + str(trial.get('spheres')[i].get('r')) + "\n")
		outfile2.close()
	except IOError:
		viz.logWarn("Dont have the file permissions to log data")

		
	


# runs the experiment from here

myTask = viztask.schedule(executeExperiment())

	



	
	
