import viz
import vizact
import vizmat

viz.setMultiSample(4)
viz.fov(60)
viz.go()

viz.MainView.setPosition([ 0, 1, 0.5 ])

#Add objects for the shadow to be cast upon
ground = viz.addChild( 'ground.osgb' )

#Sphere to have the shadow cast upon
import vizshape
ball = vizshape.addSphere()
ball.setPosition([0,2,4])

ball2 = vizshape.addSphere()
ball2.setPosition([3,2,4])
ball2.setScale(2,2,2)

soccer = viz.addTexture("VRStuff\grid.jpg")
soccer.wrap(viz.WRAP_T, viz.REPEAT)

matrix = vizmat.Transform()
matrix.setScale([2,2,2])
ball2.texmat( matrix )

soccer2 = viz.addTexture('VRStuff\grid.jpg')
soccer2.wrap(viz.WRAP_T, viz.REPEAT)
soccer2.wrap(viz.WRAP_S, viz.REPEAT)


ball.texture(soccer2)
#ball.setScale(2,2,2)
ball2.texture(soccer2)



