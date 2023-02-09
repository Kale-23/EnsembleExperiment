import viz
import vizact


viz.setMultiSample(4)
viz.fov(60)
viz.go()

import vizinfo
vizinfo.InfoPanel()

viz.MainView.setPosition([ 0, 1, 0.5 ])

#Add objects for the shadow to be cast upon
ground = viz.addChild( 'ground.osgb' )

#Sphere to have the shadow cast upon
import vizshape
ball = vizshape.addSphere()
ball.setPosition([0,2,4])

ball2 = vizshape.addSphere(radius=2)
ball2.setPosition([3,2,4])

soccer = viz.addTexture("VRStuff\soccer.jpg")

#soccer.wrap(viz.WRAP_S, viz.REPEAT)
#soccer.wrap(viz.WRAP_T, viz.REPEAT)

ball.texture(soccer)
ball2.texture(soccer)

