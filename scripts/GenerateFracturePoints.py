# GenerateFracturePoints
# My first try for to generate fracture points in the table

import maya.cmds as cmds
import random
import math

# Get object to be shattered (our table)
cmds.select('roundTable')
selected = cmds.ls(sl=True, transforms=True)
obj = selected[0]
print(obj)

# Get center point of collision (in our case center of table board)
comTable = (0, 5, 0) #cmds.objectCenter('tableBoard', gl=True)
numPoints = 100
fractureRadius = 2
thickness = 0.5 #cmds.getAttr('tableBoard.height')
height = 5 #cmds.getAttr('tableBoard.translateY')
voroX = []
voroY = []
voroZ = []

# Help function
def surfaceMaterial(obj, R, G, B):
    name = (obj + '_shardMaterial')
    if ( cmds.objExists(name) == 0 ):
        cmds.shadingNode( 'lambert', asShader = True, name = name )
        cmds.sets( renderable = True, noSurfaceShader = True, empty = True, name = (name + 'SG'))
        cmds.connectAttr( (name + '.outColor'), (name + 'SG.surfaceShader'), force = True)
        cmds.setAttr((name + '.color'), R, G, B, type = "double3") 
    return name

# A Normal/Gaussian distribution centered in the middle of the table gives our sample points
for i in range(numPoints):
    r = random.gauss(0, fractureRadius)
    theta = random.random() * 2 * math.pi
    voroX.append(r * math.cos(theta))
    # Translate the generated point in z-axis to simulate wooden fibers
    voroZ.append(r * math.sin(theta) * 2) 
    voroY.append((random.random() * thickness) + height)

voroPoints = zip(voroX, voroY, voroZ)
surfaceMat = surfaceMaterial(obj, 0.5, 0.5, 1)
#print(voroPoints)

# Set up progress bar
cmds.progressWindow(title = "Voronoi Calculating", progress = 0, isInterruptable = True, maxValue = numPoints)
cmds.undoInfo(state = False)
cmds.setAttr(obj + '.visibility', 0)
step = 0
chunksGrp = cmds.group( em=True, name = str(obj) + '_chunks_1' )

# Use voronoi diagrams to create cuts
for startPoint in voroPoints:
    # Update progress bar
    if cmds.progressWindow(q=True, isCancelled=True ): break
    if cmds.progressWindow(q=True, progress=True ) >= numPoints: break
    step = step + 1    
    cmds.progressWindow( edit=True, progress=step, status=("Shattering step %d of %d completed..." % (step, numPoints)) )
    cmds.refresh()


    # Duplicate object to create splinters
    workingGeom = cmds.duplicate(obj)
    cmds.setAttr(str(workingGeom[0])+'.visibility', 1)
    cmds.parent(workingGeom, chunksGrp)
    
    for endPoint in voroPoints:
        if startPoint != endPoint:
            # Construct line segments and calculate the mid point and its normal
            aimVec = [(pt1-pt2) for (pt1, pt2) in zip(startPoint, endPoint)]
            centerPoint = [(pt1 + pt2)/2 for (pt1, pt2) in zip(startPoint, endPoint)]
            planeAngle = cmds.angleBetween( euler=True, v1=[0,0,1], v2=aimVec )
            
            # Cut Geometry (Bullet shatter)
            cmds.polyCut(workingGeom[0], df=True, cutPlaneCenter = centerPoint, cutPlaneRotate = planeAngle)
            
            # Applying the material to the cut faces
            oriFaces = cmds.polyEvaluate(workingGeom[0], face=True)
            cmds.polyCloseBorder(workingGeom[0], ch=False)
            aftFaces = cmds.polyEvaluate(workingGeom[0], face=True)
            newFaces = aftFaces - oriFaces
         
            cutFaces = ( '%s.f[ %d ]' % (workingGeom[0], (aftFaces + newFaces - 1)))
            cmds.sets(cutFaces, forceElement = (surfaceMat + 'SG'), e=True)
            

    cmds.xform(workingGeom, cp=True)
    print str(workingGeom)
        
cmds.xform(chunksGrp, cp=True)
cmds.progressWindow(endProgress=1)
cmds.undoInfo(state = True)





