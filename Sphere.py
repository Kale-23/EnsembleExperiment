import viz
import viztask
import vizact
import vizshape
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

#sphere parameters
rMean = 0.5 #mean of radius of spawned spheres (in meters) mean will differ slightly from this number in each trial
rSTD = 0.1 #standard deviation of the radius of spawned spheres (in meters)
sphereCount = 20 #how many spheres to spawn in each trial
trialCount = 10 #how many trials to complete
sphereShowTime = 5 #seconds to show sphere before disappearing

#where spheres will show up
leftX = -5 #left bounding wall for spawned spheres
rightX = 5 #right bounding wall for spawned spheres
bottomY = 1 #bottom bounding wall for spawned spheres
topY = 5 #top bounding wall for spawned spheres
distance = 10 #distance from (0,0, 0) in the z direction to spawn the spheres

#globals
spheres = [] #will contain all sphere parameters stored in individual dictionaries
spheresInEnv = [] #will contain sphere objects that are currently being showed to participant

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
returns average of spheres
'''
def getAverageRadius():
	tempList = []
	for s in spheres:
		tempList.append(s.get('r'))
	return mean(tempList)

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

''' TODO remove after testing probably
removes all speheres in spheresInEnv list from environment
* removes spheres from environemt
* makes new spheres
* adds new spheres to environent
'''
def reset(key):
	if key == ' ':
		for s in spheresInEnv:
			s.remove()
		makeSpheres()
		addSpheres()
		
		
# For testing TODO remove
def resetNoKey():
	for s in spheresInEnv:
		s.remove()

''' TODO remove after testing
probably put all experiment stuff in here
'''
def testing():
	#tempList = []
	###templist.append
	yield viztask.waitKeyDown(' ') 
	# yield viztask.waitTime(2)
	makeSpheres()
	addSpheres()
	viz.callback(viz.KEYDOWN_EVENT,reset)



def executeExperiment():
	experiment = []
	
	for trialNumber in range(trialCount):
		yield makeSpheres()
		sphereParams = spheres
		rad = getAverageRadius()
		yield addSpheres()
		yield viztask.waitTime(sphereShowTime)
		yield resetNoKey()
				
		trial = {
		'trialNumber': trialNumber + 1,
		'spheres': sphereParams,
		'averageRadius': rad,
		#'guessedRadius': int
		}
		
		experiment.append(trial)
		print("trial done: ", trialNumber)
	print("done all")
	print(experiment)



# runs the experiment from here

myTask = viztask.schedule(executeExperiment())
vizact.onkeydown( 'e', myTask.kill )
#viztask.schedule(testing())

	



	
	
