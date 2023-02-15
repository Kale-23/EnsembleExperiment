import viz
import viztask
import vizact
import vizshape
import vizinfo

import steamvr
import vizdlg

import random
import math
from statistics import mean
import os

https://elvers.us/perception/visualAngle/va.html

##### GLOBALS #####
###################

participantHeight = 0 #recorded during learning phase

# These adjust the number of trials of each distannce, and how far the spheres are shown on the z axis from zero
learningCount = 1 # How many trials for each distance in learning phase
count = 2 # How many trials for each distance in experimental phase
distance1 = 6 # Distance from zero of foreground trials
distance2 = 12 # Distance from zero of Middle trials
distance3 = 18 # Distance from zero of Background trials

# These adjust the parameters for the imaginary circumferencne the spheres are placed on
cirlceRadius = 2 # Radius of circumference
circleCenterX = 0 # where the center of the circumference will be placed on the x axis
jitter = 5 # degrees the spheres can jitter from thier placement angle (ie with jitter = 5, the sphere at 0 degrees will be randomly placed between 355 degrees and 5 degrees)

# Pause times between events of experiment
trialShowPause = 1 #time to pause after showing the trial spheres
fixationShowPause = 0.5 #time the fixation point is on screen before spheres show
betweenTrialPause = 0 #time between submission of probe sphere and next trial start

# Radius values for spheres
rLow = 0.2 # Lowest radius a sphere can randomly be given
rHigh = 0.4 # Highest radius a sphere can randomly be given
rAvgLow = 0.25 # minimum average radius for spheres in each trial, if below this value sphere values for trial will be deleted and new values will be generated
rAvgHigh = 0.35 # maximum average radius for spheres in each trial, if above this value, sphere values for trial will be deleted ad ew values will be generated

# probe parameters
probeRadLow = 0.25 # Lowest radius the probe can randomly be given
probeRadHigh = 0.35 # Highest radius the probe can randomly be given
scale_factor = 1 # factor by which the radius of the probe will be scaled by when shown.
valueToScaleBy = 1.005 # value by which the scale factor of the probe is increased/decreased during response

# response parameters
endResponseInput = steamvr.BUTTON_TRIGGER # participant input that confirms their probe size and ends response portion of trial.
timeToScale = 60 # max time participant has to scale probe sphere and submit answer.

# global lists
sphereList = [] # All spheres and trials are pregenerated before running the experiment, each trial is stored in this list. The trials stored will be lists of 8 sphere parameters per trial.
spheresOut = [] # Will hold any sphere entity that is currently being shown in the environment, is emptied anytime removeSpheres is called
trialProbeResponse = [] # holds the data of participant probe sphere responses for each trial (probeRadius, probeResponseTime).
data = [] # holds participant data collected at end in info panel

#texture mapping for spheres and probe
texture = False #apply texture to spheres and probe
grid = viz.addTexture('VRStuff\grid.jpg') #importing the texture file
grid.wrap(viz.WRAP_T, viz.REPEAT) #next two make it so texture repeats, size of texture stays the same while size of object changes
grid.wrap(viz.WRAP_S, viz.REPEAT)
matrix = vizmat.Transform() #adjusted when spheres are made, makes it so texture maps correctly onto objects

##### METHODS #####
###################

'''
Creates the '+' fixation point. Set to show at 'distance2' for all trials to create depth. 
'''
def showFixationPoint():
	global spheresOut
	global distance2
	
	box1 = vizshape.addBox(size=(0.25, 0.05, 0.05), color = viz.WHITE)
	box2 = vizshape.addBox(size=(0.05, 0.25, 0.05), color = viz.WHITE)
	box1.setPosition(0,participantHeight,distance2)
	#box1.setScale([dist / distance2, dist / distance2, dist / distance2])
	box2.setPosition(0,participantHeight,distance2)
	#box2.setScale([dist / distance2, dist / distance2, dist / distance2])
	spheresOut.append(box1)
	spheresOut.append(box2)

'''
Creates 8 spheres for each trial. 
Sphere parameters will be gennerated every 45 degrees (+/- 'jitter') around the imaginary circumference starting at 0 degrees up to 315 degrees. 
The imaginary circumference will always appear to be the same size no matter the distance from the participant.
If the average radius of all 8 spheres is between 'rAvgLow' and 'rAvgHigh', the trial is accepted and added to 'sphereList', else it is thrown out and new parameters are chosen.
'''
def makeSpheres(count, distance, rL, rH, slist):
	
	'''
	finds the x value within the imaginary circumference to place the sphere at. 
	'''
	def getX(angle, distance):
		return circleCenterX + ((cirlceRadius * distance) * math.cos(angle))

	'''
	finds the y value within the imaginary circumferecne to place the sphere at. 
	'''
	def getY(angle, distance):
		return participantHeight + ((cirlceRadius * distance) * math.sin(angle))

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
			slist.append(spheres)
			tempCount += 1
	

'''
takes a list of sphere parameters, adds them to the environment, and adds them to 'spheresOut'.
'''
def addSpheres(spheres):
	global spheresOut
	global grid
	global matrix
	
	for s in spheres:
		rad = s[3] * (s[2] / distance2) # radius adjusted for distance, also used to scale matrix for texturing
		sphereAdd = vizshape.addSphere(rad)
		sphereAdd.lighting = True
		if texture:
			matrix.setScale([rad, rad, rad])
			sphereAdd.texmat( matrix )
			sphereAdd.texture(grid)
		sphereAdd.setPosition(s[0], s[1], s[2])
		spheresOut.append(sphereAdd)

'''
removes objects (spheres, fixation point, and probe) from environment when called
'''
def removeSpheres():
	global spheresOut
	
	for s in spheresOut:
		s.remove()
	spheresOut = []
	
'''
creates and shows probe sphere always at 'distance2'.
The probe's radius is random between 'probeRadLow' and 'probeRadHigh'.
participant can change probe size through 'onKeyDown' using the thumbstick.
texture size stays the same while the probe size changes.
once participant calls 'endKeyDown', participant response is stopped and returned.
'''
def response(dist):
	
	'''
	this is what controls participant input
	'''
	def onKeyDown():
		'''
		will multiply 'scale_factor' by 'valueToScaleBy'.
		'''
		def increase_scale(sphere):
			global scale_factor
			scale_factor *= valueToScaleBy
			sphere.setScale([scale_factor, scale_factor, scale_factor])

		'''
		will divide 'scale_factor' by 'valueToScaleBy'.
		'''
		def decrease_scale(sphere):
			global scale_factor
			scale_factor /= valueToScaleBy
			sphere.setScale([scale_factor, scale_factor, scale_factor])
			
		if controller.getThumbstick()[1] < -0.1:
			decrease_scale(spheresOut[0])
			if texture:
				matrix.setScale([probeRadius * scale_factor, probeRadius * scale_factor, probeRadius * scale_factor])
				probe.texmat( matrix )
				probe.texture(grid)
		elif controller.getThumbstick()[1] > 0.1:
			increase_scale(spheresOut[0])
			if texture:
				matrix.setScale([probeRadius * scale_factor, probeRadius * scale_factor, probeRadius * scale_factor])
				probe.texmat( matrix )
				probe.texture(grid)
		else:
			pass


	global spheresOut
	global scale_factor
	global distance2
	global matrix
	spheresOut = []
	
	# Probe created and output to environment
	probeRadius = random.uniform(probeRadLow, probeRadHigh)
	probe = vizshape.addSphere(probeRadius)
	if texture == True:
		matrix.setScale([probeRadius, probeRadius, probeRadius])
		probe.texmat( matrix )
		probe.texture(grid)
	probe.setPosition(0, participantHeight, distance2)
	spheresOut.append(probe)
	
	# Set the initial scaling factor for the probe in this trial
	scale_factor = 1.0

	# Allows participant input during this time until 'endResponseInput' is input.
	responseUpdater = vizact.onupdate(0, onKeyDown)
	responded = viztask.waitSensorDown(controller, endResponseInput)
	waitTime = viztask.waitTime(timeToScale)
	
	#waits until participant responds or time limit is reached, then stops participant input
	time = yield viztask.waitAny([waitTime,responded])
	responseUpdater.setEnabled(viz.OFF)
	
	#output of variables, determines if participant responded or not
	noResponse = 0
	if time.condition == waitTime:
		noResponse = 1
	
	viztask.returnValue([probeRadius, scale_factor, probeRadius * scale_factor, noResponse])
	
'''
participant gets introduction to thier task
participant orientationa and height set, and height is recorded
lighting and floor output to environment (?)
learning trials occur
'''
def learningPhase():
	
	# addRayPrimitive from @ischtz on github
	def addRayPrimitive(origin, direction, length=100, color=viz.RED, alpha=0.6, linewidth=3, parent=None):
		""" Create a Vizard ray primitive from two vertices. Can be used
		to e.g. indicate a raycast or gaze vector in a VR environment.
		
		Args:
			origin (3-tuple): Ray origin
			direction (3-tuple): Unit direction vector
			length (float): Ray length (set to 1 and use direction=<end>
				to draw point-to-point ray)
			color (3-tuple): Ray color
			alpha (float): Ray alpha value
			linewidth (int): OpenGL line drawing width in pixels
			parent: Vizard node to use as parent
		"""
		viz.startLayer(viz.LINES)
		viz.lineWidth(linewidth)
		viz.vertexColor(color)
		viz.vertex(origin)
		viz.vertex([x * length for x in direction])
		ray = viz.endLayer()
		ray.disable([viz.INTERSECTION, viz.SHADOW_CASTING])
		ray.alpha(alpha)
		if parent is not None:
			ray.setParent(parent)
		return ray
	
	#participant sees instructions
	instructions = """Your task is to estimate the average size of spheres. 
You will be shown a fixation point, which you must focus on.
Spheres will appear around the fixation point, but please stay focused 
on the fixation point. After a short time, the spheres will
dissapear, and a new sphere will appear. Using your controller,
you can press down to make the sphere smaller, and up
to make it larger. To the best of your ability, make the size
of this sphere match the average size of the previous spheres.

Press the trigger button when you are ready to continue"""
	panel = viz.addText(instructions)
	panel.alignment(viz.ALIGN_LEFT_CENTER)
	panel.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
	panel.resolution(1)
	panel.disable(viz.LIGHTING)
	panel.font('Arial')
	panel.fontSize(4)
	textLink = viz.link(viz.MainView,panel,mask=viz.LINK_POS)
	textLink.setOffset([-50,0,100])
	#instructor sees info
	info = vizinfo.InfoPanel("Participant is reading tutorial.")
	info.visible(viz.ON)
	#wait for conformation and removes info panels
	yield viztask.waitSensorDown(controller, [steamvr.BUTTON_TRIGGER])
	info.remove()
	panel.remove()
	
	yield viztask.waitTime(0.5) #test timing, mainly so no accidental skip of next instruction panel
	
	instructions = """Please line yourself with your head directly over 
the blue line below, and make yourself comfortable
in your chair. The position you are in now will have
to be held throughout the experiment, so that your
height and orientation remains constant. Please stay in 
this position until the experiment is over.

Press the trigger button when you are in position and ready to continue"""
	panel = viz.addText(instructions)
	panel.alignment(viz.ALIGN_LEFT_CENTER)
	panel.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
	panel.resolution(1)
	panel.disable(viz.LIGHTING)
	panel.font('Arial')
	panel.fontSize(4)
	textLink = viz.link(viz.MainView,panel,mask=viz.LINK_POS)
	textLink.setOffset([-50,0,100])
	
	spheresOut.append(addRayPrimitive(origin=[0,0.001,0], direction=[0,0.001,1], color=viz.BLUE)) #for alignment of participant
	
	info = vizinfo.InfoPanel("Participant is about to take height.")
	info.visible(viz.ON)
	yield viztask.waitSensorDown(controller, [steamvr.BUTTON_TRIGGER])
	info.remove()
	panel.remove()
	removeSpheres() #removes alignment ray
	
	#taking participant height
	global participantHeight
	participantHeight = viz.MainView.getPosition()[1]
	
	yield viztask.waitTime(0.5)
	
	instructions = """You will now begin with practice trials.
The instructor can provide guidance on
these practice trials. You will be notified again
when the experimental trials begin.

Press the trigger button when you are ready to start"""
	panel = viz.addText(instructions)
	panel.alignment(viz.ALIGN_LEFT_CENTER)
	panel.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
	panel.resolution(1)
	panel.disable(viz.LIGHTING)
	panel.font('Arial')
	panel.fontSize(4)
	textLink = viz.link(viz.MainView,panel,mask=viz.LINK_POS)
	textLink.setOffset([-50,0,100])
	info = vizinfo.InfoPanel("Participant is begining practice trials.")
	info.visible(viz.ON)
	yield viztask.waitSensorDown(controller, [steamvr.BUTTON_TRIGGER])
	info.remove()
	panel.remove()
	
	#set lighting for experiment
	headLight = viz.MainView.getHeadLight()
	headLight.disable()
	light = viz.addLight()
	light.enable()
	light.direction(0,0,1)
	light.position(0,participantHeight,0)
	light.spread(180)
	light.intensity(1.5)
	
	#setting the environment for trials such as floor, wall, etc if wanted
	floorGrid = vizshape.addGrid(size=(40, 40), axis=vizshape.AXIS_Y, pos=(0,-2.5,0))
	#floor = vizshape.addPlane(size=(2.0,2.0),axis=vizshape.AXIS_Y,cullFace=True, lighting=True, pos=(0,0,0))
	#wall = vizshape.addPlane(size=(50,50),axis=vizshape.AXIS_Z,cullFace=True, lighting=True, pos=(0,0,20), flipFaces=True)
	
	learningList = []
	makeSpheres(learningCount, distance1, rLow, rHigh, learningList)
	makeSpheres(learningCount, distance2, rLow, rHigh, learningList)
	makeSpheres(learningCount, distance3, rLow, rHigh, learningList)
	random.shuffle(learningList)
	
	for i in range(len(learningList)): # runs through all trials stored in 'sphereList'
		print(learningList[i][0][2])
		yield showFixationPoint() #shows fixation cross
		yield viztask.waitTime(fixationShowPause) #pause
		yield addSpheres(learningList[i]) #shows trial spheres
		yield viztask.waitTime(trialShowPause) #pause
		yield removeSpheres() #removes cross and spheres
		
		yield response(learningList[i][0][2]) #response portion of trial is performed, returned values not recorded
		yield removeSpheres() #removes probe sphere
	
	
	instructions = """The learning phase is
over. The experiment will now begin.
If you have any last questions, please ask now.

Press the trigger button when you are ready to start"""
	panel = viz.addText(instructions)
	panel.alignment(viz.ALIGN_LEFT_CENTER)
	panel.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
	panel.resolution(1)
	panel.disable(viz.LIGHTING)
	panel.font('Arial')
	panel.fontSize(4)
	textLink = viz.link(viz.MainView,panel,mask=viz.LINK_POS)
	textLink.setOffset([-50,0,100])
	info = vizinfo.InfoPanel("Participant is begining experimental trials.")
	info.visible(viz.ON)
	yield viztask.waitSensorDown(controller, [steamvr.BUTTON_TRIGGER])
	info.remove()
	panel.remove()
	
"""
creates info panel that allows participant input
records age, gender, handedness, vision
"""
def participantInfo():
	
	info = vizinfo.InfoPanel("", title = "Please put in your information", margin = (100, 100), align = viz.ALIGN_CENTER_TOP) #will have to adjust for vr headset
	
	#handedness
	rightHanded = info.addLabelItem('Right Handed', viz.addRadioButton('handed'))
	leftHanded = info.addLabelItem('Left Handed', viz.addRadioButton('handed'))
	
	#age
	info.addSeparator()
	ages = []
	age = info.addLabelItem('Age',viz.addDropList())
	for i in range(18,40):
		ages.append(str(i))
	age.addItems(ages)
	
	#gender
	info.addSeparator()
	female = info.addLabelItem('female', viz.addRadioButton('gender'))
	male = info.addLabelItem('male', viz.addRadioButton('gender'))
	other = info.addLabelItem('other', viz.addRadioButton('gender'))
	none = info.addLabelItem('prefer not to say', viz.addRadioButton('gender'))
	
	#vision
	info.addSeparator()
	noneLenses = info.addLabelItem('none', viz.addRadioButton('glasses'))
	glasses = info.addLabelItem('glasses', viz.addRadioButton('glasses'))
	correctiveLenses = info.addLabelItem('corrective lenses', viz.addRadioButton('glasses'))
	
	#submit button
	info.addSeparator()
	submitButton = info.addItem(viz.addButtonLabel('Submit'),align=viz.ALIGN_RIGHT_CENTER)
	yield viztask.waitButtonUp(submitButton)
	
	handedData = ''
	if rightHanded.get() == viz.DOWN:
		handedData = 'right'
	else:
		handedData = 'left'
	ageData = age.getSelection()
	genderData = ''
	if female.get() == viz.DOWN:
		genderData = 'female'
	elif male.get() == viz.DOWN:
		genderData = 'male'
	elif other.get() == viz.DOWN:
		genderData = 'other'
	else:
		genderData = 'noAnswer'
	visionData = ''
	if noneLenses.get() == viz.DOWN:
		visionData = 'none'
	elif glasses.get() == viz.DOWN:
		visionData = 'glasses'
	else:
		visionData = 'correctiveLenses'
	
	data = [handedData, ageData + 18, genderData, visionData]
	
	info.remove()
	viztask.returnValue(data)

"""
creates variables for headset, controller.
links these to the main view.
"""
def vrSetup():
	#headset
	hmd = steamvr.HMD()
	if not hmd.getSensor():
		sys.exit('SteamVR HMD not detected')
		
	navigationNode = viz.addGroup()
	viewLink = viz.link(navigationNode, viz.MainView)
	viewLink.preMultLinkable(hmd.getSensor())
		
	#controller
	global controller
	for controller in steamvr.getControllerList():
		controller.model = controller.addModel(parent=navigationNode)
		controller.model.disable(viz.INTERSECTION)
		viz.link(controller, controller.model)
		
		viz.startLayer(viz.LINES)
		viz.vertexColor(viz.WHITE)
		viz.vertex([0,0,0])
		viz.vertex([0,0,100])
		controller.line = viz.endLayer(parent=controller.model)
		controller.line.disable([viz.INTERSECTION, viz.SHADOW_CASTING])
		controller.line.visible(False)#if it's set to true then we'll always see the controlller liner
	
	
	
'''
for each trial in 'sphereList':
The fixation point will be shown for 'fixationShowPause' seconds.
The spheres of the trial will show for 'trialShowPause' seconds.
Both the fixation point and spheres will be taken off the screen, and the probe will appear.
The participant is allowed to adjust the size of the probe until they are satisfied, and then the probe is taken off the screen.
'''
def experiment():
	global SphereList
	global trialProbeResponse
	
	global data
	data = yield participantInfo()
	
	vrSetup()
	#learning phase/ records participant height
	yield learningPhase()
	
	##grey grid setup
	#grid = vizshape.addGrid(boldStep=0)
	#grid.color(viz.GRAY)
	
	
	#have to be made after learning phase so height is accurate
	makeSpheres(count, distance1, rLow, rHigh, sphereList)
	makeSpheres(count, distance2, rLow, rHigh, sphereList)
	makeSpheres(count, distance3, rLow, rHigh, sphereList)
	random.shuffle(sphereList)

	#testing phase, runs through all trials
	for i in range(len(sphereList)): # runs through all trials stored in 'sphereList'
		print(sphereList[i][0][2])
		yield showFixationPoint() #shows fixation cross
		yield viztask.waitTime(fixationShowPause) #pause
		yield addSpheres(sphereList[i]) #shows trial spheres
		yield viztask.waitTime(trialShowPause) #pause
		yield removeSpheres() #removes cross and spheres
		
		startTime = viz.tick() #starts timing response time
		probe = yield response(sphereList[i][0][2]) #response portion of trial is performed
		responseTime = viz.tick() - startTime #response time is recorded
		resp = [probe, responseTime]
		trialProbeResponse.append(resp)
		yield removeSpheres() #removes probe sphere
		
	#lets the participant know the experiment is over
	instructions = """The experiment is now over
you may remove the headset and controller.
Thank you for your time."""
	
	panel = viz.addText(instructions)
	panel.alignment(viz.ALIGN_LEFT_CENTER)
	panel.setBackdrop(viz.BACKDROP_RIGHT_BOTTOM)
	panel.resolution(1)
	panel.disable(viz.LIGHTING)
	panel.font('Arial')
	panel.fontSize(4)
	textLink = viz.link(viz.MainView,panel,mask=viz.LINK_POS)
	textLink.setOffset([-50,0,100])
	
		#takes information and writes to new file
	writeOut()
	print("experiment over")



'''
Creates new file and records trial, sphereNumber, sphereX, sphereY, sphereDist, sphereRadius, probeAnswerRadius, probeAnswerTime for each sphere within a trial, for each trial.
'''
def writeOut():
	
	'''
	automatically gets and updates the current participant number for naming output file.
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
	outputs each trial sphere to string format that works with csv output
	'''
	def sphereToString(s):
		tempString = ""
		for i in range(len(s)):
			tempString += "(" + str(s[i][0]) + ";" + str(s[i][1]) + ";" + str(s[i][2]) + ";" + str(s[i][3]) + "),"
		return tempString[0:-1]

	'''
	gets average of trial sphere radii for a trial
	'''
	def sphereTrialAverageRadius(s):
		total = 0
		for i in range(len(s)):
			total += s[i][3]
		return total / len(s)
	
	path = "participantData"
	participantNumber = getParticipantNumber()
	
	if not os.path.exists(path):
		os.makedirs(path)

	filename = "Participant" + str(participantNumber) + ".csv"
	with open(os.path.join(path, filename), 'w') as outfile:
		try:
			outfile.write("ID,age,gender,hand,vision,height,trial,sphereOne,sphereTwo,sphereThree,sphereFour,sphereFive,sphereSix,sphereSeven,sphereEight,sphereDistance, sphereAverageRadius,probeStartingRadius,probeAnswerRadius,probeScaleFactor,probeResponseTime,probeResponseOverTimeLimit\n")
			
			for i in range(len(sphereList)):
				outfile.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(participantNumber, data[1], data[2], data[0], data[3], participantHeight, i + 1, sphereToString(sphereList[i]), sphereList[i][0][2], sphereTrialAverageRadius(sphereList[i]), trialProbeResponse[i][0][0], trialProbeResponse[i][0][2], trialProbeResponse[i][0][1], trialProbeResponse[i][1], trialProbeResponse[i][0][3]))
		
		except IOError:
			viz.logWarn("Dont have the file permissions to log data")



##### MAIN #####
################

if __name__ == '__main__':
	
	#setup
	viz.setMultiSample(4)
	viz.fov(60)
	viz.go()
	
	#experiment run from here
	theExperiment = viztask.schedule(experiment())
	
