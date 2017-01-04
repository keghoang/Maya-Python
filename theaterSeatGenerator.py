import maya.cmds as cmds
import math
import random
import functools

def createUI( pWindowTitle, pApplyCallback ) :

    windowID = 'Seat Generator'

    if cmds.window( windowID, exists=True ) :
        cmds.deleteUI( windowID )

    cmds.window( windowID, title=pWindowTitle, sizeable=True, resizeToFitChildren=True )
    cmds.columnLayout(adj=True)
    cmds.separator( h=10, style='none' )
    
    distanceAmount = cmds.intSliderGrp(l = "Distance Between", min = 1, max = 10, value = 1, field = True)
    
    cmds.separator( h=10, style='none' )
    
    bridgeHeight = cmds.intSliderGrp(l = "Bridge Height", min = 1, max = 7, value = 5, field = True)
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    
    cmds.button( label='Apply', command=functools.partial( pApplyCallback, distanceAmount, bridgeHeight ) )
        
    def cancelCallback( *pArgs ):
        if cmds.window( windowID, exists=True ) :
            cmds.deleteUI( windowID )
    
    cmds.button( label='Cancel', command=cancelCallback )
    cmds.showWindow()

def calculateXlength( shapeNode ) :

    bbox = cmds.xform( shapeNode, query=True, bb=True )
    Xlength=abs( bbox[3]-bbox[0] )
    
    return Xlength

def calculateYlength( shapeNode ) :

    bbox = cmds.xform( shapeNode, query=True, bb=True )
    Ylength=abs( bbox[4]-bbox[1] )
    
    return Ylength

def calculateZlength( shapeNode ) :

    bbox = cmds.xform( shapeNode, query=True, bb=True )
    Zlength=abs( bbox[5]-bbox[2] )
    
    return Zlength  
    
def applyCallback( pDistanceAmount, pBridgeHeight, *pArgs ):
    
    distance = cmds.intSliderGrp( pDistanceAmount, query=True, value=True) / 20.
    bridgeHeight = 1 / (cmds.intSliderGrp( pBridgeHeight, query=True, value=True) / 10.)
    
    
    fenceList = cmds.ls( 'grp_seatInstance' )
    if len( fenceList ) > 0 :
         cmds.delete( fenceList )

    fenceModels = cmds.listRelatives( "ta_prop_theater_seat:grp_prop_theater_seat_variations" ) #need to be at origin
    
    cmds.rebuildCurve('curve', ch=True , rpo=True, rt=False, end=True, kr=False, kcp=False, kep=True, kt=False, s=14, d=1, tol=0.01)
    
    curLen = cmds.arclen( 'curve' )
    bridgeLengthRatio = calculateZlength ('bridgeModel_01') / curLen
    
    axisPerpendicularToCurve = [0, 1, 0]
    axisParallelToCurve = [0, 0, 1]
    applyRotationToAxes = [0, 1, 0]
        
    fenceCounter = 0
    u = 0.0
    
    while ( u <= 1.0 ) :
       
        fenceCounter += 1
        p = cmds.pointOnCurve('curve', pr=u, top=True)
        t = cmds.pointOnCurve('curve', pr=u, nt=True, top=True)
        n = cmds.pointOnCurve('curve', pr=u, nn=True, top=True)
        
		
        object = random.choice(fenceModels) 
        newFence = cmds.instance(object, name='seatInstance_#')
            
        # Matching fence to curvature
        rot = cmds.angleBetween(v1=axisPerpendicularToCurve, v2=t, er=True)
        rot = [ rot[0] * applyRotationToAxes[0],
                rot[1] * applyRotationToAxes[1],
                rot[2] * applyRotationToAxes[2]]

        cmds.xform(newFence, t=p, ws=True, a=True)          
        cmds.xform(newFence, ro=rot, ws=True)

        # Random relative rotation
        randX = random.random() * 10.
        randY = random.random() * 2.
        randZ = random.random() * 10.
        cmds.xform(newFence, ro=[randX, randY, randZ], r=True)  
       
        # Random relative scale
        randX = 1.0
        randY = random.uniform(-0.1,0.1) + 1.0
        randZ = 1.0
        cmds.xform(newFence, r=True, s=[randX, randY, randZ])
        
        u += distance
       
    fenceList = cmds.ls( 'seatInstance_*' )
    cmds.group(fenceList, name='grp_seatInstance')     
    cmds.select( clear=True)

createUI( 'Seater', applyCallback ) 