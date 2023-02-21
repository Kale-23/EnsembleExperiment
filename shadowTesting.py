import viz
import viztask
import vizact
import vizshape
import vizinfo

import projector

import random
import math
from statistics import mean

#setup
viz.setMultiSample(4)
viz.fov(60)
viz.go()
viz.MainView.setPosition(0, 3, 0)

#grey grid on floor TODO remove after testing
ground = viz.addChild( 'ground.osgb' )

sphere = vizshape.addSphere(radius=1)
sphere.setPosition(0,3,4)

shadow = projector.add( viz.addTexture('shadow.jpg'))
shadow.setEuler([0,90,0])

shadow.affect(ground)


eyeBalls.ortho( 0.25, 0.15 )

sphere.setParent(shadow)
sphere.setPosition([ 0, 1, 3 ])


