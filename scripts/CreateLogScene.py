# CreateLogScene.py
# Starting script: Create 3 old wooden logs

import maya.cmds as cmds
import maya.app.mayabullet.RigidBody as RigidBody
BulletUtils.checkPluginLoaded()

# Create the logs and set them as active rigid bodies
log1 = cmds.polyCylinder(r=2.5, h=12, sx=40, sy=20, sz=20, ax=(0, 0, 1), name='log1', ch=0, cuv=3)
cmds.setAttr('log1.translateY', 50)
#cmds.setAttr('log1.translateX', 5)
#cmds.rigidBody(active=True, mass=5, b=0)

log2 = cmds.polyCylinder(r=2.5, h=16, sx=40, sy=20, sz=20, ax=(0, 0, 1), name='log2', ch=0, cuv=3)
cmds.setAttr('log2.translateY', 70)
cmds.setAttr('log2.rotateY', 25)
#cmds.rigidBody(active=True, mass=7.5, b=0)

log3 = cmds.polyCylinder(r=3.5, h=12, sx=40, sy=20, sz=20, ax=(0, 0, 1), name='log3', ch=0, cuv=3)
cmds.setAttr('log3.translateY', 100)
cmds.setAttr('log3.translateX', 5)
cmds.setAttr('log3.rotateY', 90)
#cmds.rigidBody(active=True, mass=10, b=0)

# Create passiv floor
floor = cmds.polyPlane(h=55, w=55, sx=10, sy=10, ax=(0, 1, 0), name='floor', cuv=2, ch=0)
#cmds.rigidBody(passive=True, bounciness=0.02, layer=-1)
RigidBody.CreateRigidBody(False).executeCommandCB()

# Add dynamics (gravity)
grav = cmds.gravity(pos=(0, 0, 0), m=9.8, dx=0, dy=-1, dz=0, att=0, mxd=-1, name='myGravity')
#cmds.connectDynamic( 'log1', 'log2', 'log3', f='myGravity' )

# Add some light
cmds.directionalLight(name='dirLight', decayRate=2, intensity=90, rgb=(1.0, 0.8, 0.8), rotation=(45, 70, 60))

