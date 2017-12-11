# TranslateThroughTable

import maya.cmds as cmds


def translateThroughTable( pObjectName, pStartTime, pEndTime, pTargetAttribute, startValue, endValue ):
    # Remove existing keys
    cmds.cutKey( pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute )
    
    cmds.setKeyframe( pObjectName, time=pStartTime, attribute=pTargetAttribute, value=startValue )
    cmds.setKeyframe( pObjectName, time=pEndTime, attribute=pTargetAttribute, value=endValue )  
    cmds.selectKey( pObjectName, time=(pStartTime, pEndTime), attribute=pTargetAttribute, keyframe=True )  
    #cmds.keyTangent( inTangentType='linear', outTangentType='linear' )
    



# Set animation keyframes at start and end of playback
startTime = 0 #cmds.playbackOptions( ast=0, aet=60,  query=True, minTime=True )
endTime = 60 #cmds.playbackOptions( query=True, maxTime=True )

# Call animation
translateThroughTable('bowlingBall', startTime, endTime, 'translateY', 15, 2.5)



