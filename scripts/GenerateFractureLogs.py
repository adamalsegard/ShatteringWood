# GenerateFractureLogs
# Script to generate fracture points in the Log scene

import maya.cmds as cmds
import random
import math
import maya.app.mayabullet.BulletUtils as BulletUtils
import maya.app.mayabullet.RigidBody as RigidBody
BulletUtils.checkPluginLoaded()

# Get object to be shattered
cmds.select(['log1','log2','log3'])
selected = cmds.ls(sl=True, transforms=True)
objCounter = 0
for obj in selected: 

    print(obj)
    
    # Get center point of collision (in our case center of the logs)
    com = cmds.objectCenter(obj, gl=True)
    numPoints = 30
    fractureRadius = 3
    thickness = 1 # Will get divided by 2
    height = cmds.getAttr(obj + '.translateY')
    transX = cmds.getAttr(obj + '.translateX')
    rotY = cmds.getAttr(obj + '.rotateY')
    voroX = []
    voroY = []
    voroZ = []
    #print(height)
    
    
    # Help function 
    def surfaceMaterial(obj, R, G, B):
        name = (obj + '_shardMaterial')
        if ( cmds.objExists(name) == 0 ):
            cmds.shadingNode( 'lambert', asShader = True, name = name )
            cmds.sets( renderable = True, noSurfaceShader = True, empty = True, name = (name + 'SG'))
            cmds.connectAttr( (name + '.outColor'), (name + 'SG.surfaceShader'), force = True)
            cmds.setAttr((name + '.color'), R, G, B, type = "double3") 
        return name
    
    # A Normal/Gaussian distribution centered in the middle of the logs gives our sample points
    for i in range(numPoints):
        r = random.gauss(0, fractureRadius)
        theta = random.random() * 2 * math.pi
        voroX.append((r * math.cos(theta)) + transX)
        voroY.append((r * math.sin(theta)) + height) 
        voroZ.append((random.random()-0.5) * thickness) # [-0.5, 0.5[ * thickness
        
        '''
        temp = cmds.polyCube(name='temp'+str(obj)+str(i))
        cmds.setAttr('temp'+str(obj)+str(i)+'.translateX', voroX[i])
        cmds.setAttr('temp'+str(obj)+str(i)+'.translateY', voroY[i])
        cmds.setAttr('temp'+str(obj)+str(i)+'.translateZ', voroZ[i])
        '''
    
    voroPoints = zip(voroX, voroY, voroZ)
    surfaceMat = surfaceMaterial(obj, 1.0, 0.1, 0.4)
    #print(voroPoints)
    
    
    # Set up progress bar
    cmds.progressWindow(title = "Generating fracture shards for " + str(obj), progress = 0, isInterruptable = True, maxValue = numPoints)
    cmds.undoInfo(state = False)
    cmds.setAttr(obj + '.visibility', 0)
    step = 0
    allShards = cmds.group( em=True, name = str(obj) + '_shards' )
    
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
        cmds.select(workingGeom[0])
        #cmds.rigidBody(active=True, mass=5, bounciness=0.08, collisions=False)
        #RigidBody.CreateRigidBody(True).executeCommandCB()
        cmds.setAttr(str(workingGeom[0])+'.visibility', 1)
        cmds.parent(workingGeom, allShards)
        
        for endPoint in voroPoints:
            if startPoint != endPoint:
                # Construct line segments and calculate the mid point and its normal
                dirVec = [(pt2-pt1) for (pt1, pt2) in zip(startPoint, endPoint)]
                centerPoint = [(pt1 + pt2)/2 for (pt1, pt2) in zip(startPoint, endPoint)]
                planeAngle = cmds.angleBetween( euler=True, v1=[0,0,1], v2=dirVec )
                
                # Cut Geometry (Bullet shatter)
                cmds.polyCut(workingGeom[0], deleteFaces=True, cutPlaneCenter = centerPoint, cutPlaneRotate = planeAngle)
                
                # Applying the material to the cut faces
                originalFaces = cmds.polyEvaluate(workingGeom[0], face=True)
                cmds.polyCloseBorder(workingGeom[0], ch=False)
                resultingFaces = cmds.polyEvaluate(workingGeom[0], face=True)
                newFaces = resultingFaces - originalFaces
             
                cutFaces = ( '%s.f[ %d ]' % (workingGeom[0], (resultingFaces + originalFaces - 1)))
                cmds.sets(cutFaces, forceElement = (surfaceMat + 'SG'), e=True)
                
    
        cmds.xform(workingGeom, cp=True)
        print str(workingGeom)
            
    cmds.xform(allShards, cp=True)
    cmds.progressWindow(endProgress=1)
    cmds.undoInfo(state = True)
    
    # Create set of rigid bodies
    children = cmds.listRelatives(allShards, children=True)
    cmds.select(children)
    RigidBody.CreateRigidSet().executeCommandCB(True)
    
    solverName = 'bulletRigidSetInitialState' if objCounter == 0 else 'bulletRigidSet'+str(objCounter)+'InitialState'
    objCounter = objCounter + 1
    #solverName = str(obj) + 'SolverSetInitialState'
    #cmds.rename('bulletRigidSetInitialState', solverName)
    
    # Set bullet solver attributes
    cmds.setAttr(solverName+'.collisionShapeType', 4)
    cmds.setAttr(solverName+'.defaultMass', 8)
    cmds.setAttr(solverName+'.glueShapes', 1)
    cmds.setAttr(solverName+'.collisionShapeMargin', 0)
    cmds.setAttr(solverName+'.glueBreakingThreshold', 5)
    cmds.setAttr(solverName+'.glueMaxConstraintsPerBody', 15)

# Connect generated shards to the gravity field
#for i in range(4,33):
    #cmds.connectDynamic( 'log'+str(i), f='myGravity' )



