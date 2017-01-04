import maya.cmds as cmds
import math
import random
import functools

def createUI( pWindowTitle, pApplyCallback ) :

    windowID = 'Tile Generator'

    if cmds.window( windowID, exists=True ) :
        cmds.deleteUI( windowID )

    cmds.window( windowID, title=pWindowTitle, sizeable=True, resizeToFitChildren=True )
    cmds.columnLayout(adj=True)
    cmds.separator( h=10, style='none' )
    
    shakeAmount = cmds.intSliderGrp(l = "Shake Amount", min = 0, max = 180, field = True)
    
    cmds.separator( h=10, style='none' )
    
    displaceAmount = cmds.intSliderGrp(l = "Displace Amount", min = 0, max = 30, field = True)
    
    cmds.separator( h=10, style='none' )
    
    cutoffAmount = cmds.intSliderGrp(l = "Cutoff Amount", min = 0, max = 10, field = True)
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    
    cmds.button( label='Apply', command=functools.partial( pApplyCallback, shakeAmount, displaceAmount, cutoffAmount ) )
        
    def cancelCallback( *pArgs ):
        if cmds.window( windowID, exists=True ) :
            cmds.deleteUI( windowID )
    
    cmds.button( label='Cancel', command=cancelCallback )
    cmds.showWindow()
    
def getVtxPos( shapeNode ) :
 
    vtxWorldPosition = []
 
    vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )
 
    for i in vtxIndexList :
        curPointPosition = cmds.xform( str( shapeNode )+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )   
        vtxWorldPosition.append( curPointPosition )
 
    return vtxWorldPosition
    
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

def displaceBrick( shapeNode ) :

    rY = random.uniform( -10,10 )
    
    if ( random.randint( 0,1 )==0 ) :
    
        tZ = random.uniform( 0, ( calculateZlength( shapeNode ) / 2) ) 
        tY = random.uniform( 0, calculateYlength( shapeNode ) )
        
        rX = random.uniform( 0,10 )
        
        cmds.xform( shapeNode, t = [0, tY, -tZ] , ro = [rX, rY, 0] , r=True, worldSpace=True )
    
    else :
        
        tX = random.uniform( 0, ( calculateXlength( shapeNode ) / 2) ) 
        tY = random.uniform( 0, calculateYlength( shapeNode ) )
        
        rZ = random.uniform( 0,10 )
        
        cmds.xform( shapeNode, t = [-tX, tY, 0] , ro = [0, rY, -rZ] , r=True, worldSpace=True )
    
def applyCallback( pShakeAmount, pDisplaceAmount, pCutoffAmount, *pArgs ):
    
    shakeAmount = cmds.intSliderGrp( pShakeAmount, query=True, value=True)
    displaceAmount = cmds.intSliderGrp( pDisplaceAmount, query=True, value=True)
    cutoffAmount = cmds.intSliderGrp( pCutoffAmount, query=True, value=True)
    
    brickList = cmds.ls( 'grp_brickInstance' )
    if len( brickList ) > 0 :
        cmds.delete( brickList )

    cmds.duplicate( 'brick', name='brickModel' )
    
    brickBase = cmds.ls( 'brickModel' ) #brickBase = template brick
    ground = cmds.ls( 'ground' )
    
    brickAmountZ = int( calculateZlength(ground)/calculateZlength(brickBase) )
    brickAmountX = int( calculateXlength(ground)/calculateXlength(brickBase) ) 
    
    tempPosition = getVtxPos( 'ground' )[0]
    
    cmds.xform(brickBase, t = tempPosition, worldSpace=True)
    cmds.xform(brickBase, t = [( calculateXlength(brickBase)/2 ), ( calculateYlength( brickBase )/2 ) , -( calculateZlength( brickBase )/2 )], r=True, worldSpace=True)

    initX = cmds.getAttr( 'brickModel.translateX' )
    initZ = cmds.getAttr( 'brickModel.translateZ' )
    
    print cutoffAmount
    print brickAmountX
    
    brickCounter = 0
    cutoff_rate = brickAmountX - ( cutoffAmount/10.0 ) * brickAmountX
    createMax = brickAmountZ + 1
    
    for i in range( 1, brickAmountX+1 ) :
        
        xT = ( i-1 )*calculateXlength( brickBase ) 
        displaced = 0
        createCounter = 0
        doCreate = 0

        if ( i>=cutoff_rate ) :
            createMax -= random.randint( 0,1 )
        
        for j in range( 1, brickAmountZ+1 ) :
            
            if ( i>=cutoff_rate+1 ) :
                doCreate = random.randint( 0,1 )
                createCounter += 1
            else :
                doCreate = 1
             
            if (doCreate == 1) & ( createCounter <= createMax ) :
                
                brickCounter += 1
                cmds.instance( brickBase, name='brickInstance_#' )
                zT = ( j-1 ) * calculateZlength( brickBase )
                cmds.xform( 'brickInstance_'+str( brickCounter ), t = [xT, 0, -zT], r=True, worldSpace=True)
                
                if ( ( random.randint(0,1)==0 ) & ( random.randint( 0,1 )==0 ) & ( displaced != 1 ) ) :

                    displaceBrick ( 'brickInstance_'+str(brickCounter) )
                    displaced = 1
                    
                else :
                    if ( random.randint(0,1)==0 ) :

                        randY = 0
                        displaced = 0
                        
                        if ( random.randint(0,1)==0 ) :
                            randY = random.uniform(-1,1) * shakeAmount

                        randX = random.uniform(-1,1) * displaceAmount
                        randZ = random.uniform(-1,1) * displaceAmount
                        cmds.xform( 'brickInstance_'+str(brickCounter), ro = [randX, randY, randZ], r=True, )
                                
								
    brickList = cmds.ls( 'brickInstance_*' )
    cmds.group(brickList, name='grp_brickInstance')
    cmds.delete( 'brickModel' )
    cmds.select( clear=True)

createUI( 'Tiler', applyCallback )
