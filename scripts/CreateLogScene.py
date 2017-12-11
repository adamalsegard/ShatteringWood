# CreateLogScene.py
# Starting script: Create 3 old wooden logs

import maya.cmds as cmds

# Create the logs and set them as active rigid bodies
log1 = cmds.polyCylinder(r=2.5, h=12, sx=40, sy=20, sz=20, ax=(0, 0, 1), name='log1', ch=0, cuv=3)
cmds.setAttr('log1.translateY', 30)
cmds.rigidBody(active=True, mass=5, impulse=(0, -1, 0))

log2 = cmds.polyCylinder(r=2.5, h=16, sx=40, sy=20, sz=20, ax=(0, 0, 1), name='log2', ch=0, cuv=3)
cmds.setAttr('log2.translateY', 37)
cmds.setAttr('log2.rotateY', 45)
cmds.rigidBody(active=True, mass=10, impulse=(0, -1, 0))

log3 = cmds.polyCylinder(r=3.5, h=12, sx=40, sy=20, sz=20, ax=(0, 0, 1), name='log3', ch=0, cuv=3)
cmds.setAttr('log3.translateY', 45)
cmds.setAttr('log3.translateZ', 2)
cmds.setAttr('log3.rotateY', 90)
cmds.rigidBody(active=True, mass=15, impulse=(0, -1, 0))

# Create passiv floor
floor = cmds.polyPlane(h=55, w=55, sx=10, sy=10, ax=(0, 1, 0), name='floor', cuv=2, ch=0)
cmds.rigidBody(passive=True)

# Add dynamics (gravity)
grav = cmds.gravity(pos=(0, 0, 0), m=9.8, dx=0, dy=-1, dz=0, att=0, mxd=-1, name='myGravity')