import viz
import viztask
import vizact
import vizinfo
import vizproximity
import vizshape
import random
import math

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
leftX = -5
rightX = 5
bottomY = 1
topY = 5
rMean = 0.5
rSTD = 0.25
distance = 10
sphereCount = 10


spheres = []
spheresInEnv = []

#creates x, y, r of each sphere and stores it in a dictionary
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
			
					
# add spheres in spheres array to env, adds spheres to spheresInEnv array
def addSpheres():
	global spheresInEnv
	spheresInEnv = []
	for s in spheres:
		
		sphereAdd = vizshape.addSphere(s.get('r'))
		sphereAdd.setPosition(s.get('x'), s.get('y'), distance)
		spheresInEnv.append(sphereAdd)
	
	
#makes and adds spheres to scene, just an easier way to call both
def both():
	makeSpheres()
	addSpheres()


#reset make/ add for new set of spheres
def onKeyDown(key):
	if key == ' ':
		for s in spheresInEnv:
			s.remove()
		both()



#stuff that does stuff idk what to call it lol

both()

viz.callback(viz.KEYDOWN_EVENT,onKeyDown)



	
	
