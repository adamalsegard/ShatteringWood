# keyframeRotation.py
import maya.cmds as cmds

def keyFullRotation( pObjectName, pStartTime, pEndTime, pTargetAttribute ):
    
    cmds.cutKey( pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute )
    
    cmds.setKeyframe( pObjectName, time=pStartTime, attribute=pTargetAttribute, value=0 )
    
    cmds.setKeyframe( pObjectName, time=pEndTime, attribute=pTargetAttribute, value=360 )
    
    cmds.selectKey( pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute, keyframe=True )
    
    cmds.keyTangent( inTangentType='linear', outTangentType='linear' )


### Main script ###

selected = cmds.ls( selection=True, type='transform' )

if len( selected ) > 0:
    
    # Set animation keyframes at start and end of playback
    startTime = cmds.playbackOptions( query=True, minTime=True )
    endTime = cmds.playbackOptions( query=True, maxTime=True )
    
    #cmds.gravity(selected)
    
    for object in selected: 
        # Apply gravity!?
        # But first: Rotate!
        keyFullRotation( object, startTime, endTime, 'rotateY' )
        #applyGravity(object)
        cmds.gravity( object )
        

else: 
    print 'Please select at least one object'