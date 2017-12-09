# Starting script: Create objects

import maya.cmds as cmds

# Create table and set it to active rigid body
tableBoard = cmds.polyCylinder(r=12, h=0.5, sx=40, sy=5, sz=10, ax=(0, 1, 0), ch=0, cuv=3, name='tableBoard')
cmds.setAttr('tableBoard.translateY', 5)
leg1 = cmds.polyCylinder(r=1, h=5, sx=5, sy=5, sz=2, ax=(0, 1, 0), ch=0, cuv=3, name='leg1')
cmds.setAttr('leg1.translateX', 10)
leg2 = cmds.polyCylinder(r=1, h=5, sx=5, sy=5, sz=2, ax=(0, 1, 0), ch=0, cuv=3, name='leg2')
cmds.setAttr('leg2.translateZ', 10)
leg3 = cmds.polyCylinder(r=1, h=5, sx=5, sy=5, sz=2, ax=(0, 1, 0), ch=0, cuv=3, name='leg3')
cmds.setAttr('leg3.translateX', -10)
leg4 = cmds.polyCylinder(r=1, h=5, sx=5, sy=5, sz=2, ax=(0, 1, 0), ch=0, cuv=3, name='leg4')
cmds.setAttr('leg4.translateZ', -10)
cmds.polyUnite('tableBoard', 'leg1', 'leg2', 'leg3', 'leg4', name='roundTable')
cmds.rigidBody(active=True)

# Create bowlingball and set it as an acitve rigid bady with force downwards
ball = cmds.polySphere(r=1, sx=20, sy=20, ax=(0, 1, 0), name='bowlingBall', cuv=2, ch=0)
cmds.setAttr('bowlingBall.translateY', 15)
cmds.rigidBody(active=True, impulse=(0, -5, 0), mass=15)

# Create passiv floor
floor = cmds.polyPlane(h=35, w=35, sx=20, sy=20, ax=(0, 1, 0), name='floor', cuv=2, ch=0)
cmds.rigidBody(active=False)

# Add dynamics (gravity)
grav = cmds.gravity(pos=(0, 0, 0), m=9.8, dx=0, dy=-1, dz=0, att=0, mxd=-1, name='myGravity')