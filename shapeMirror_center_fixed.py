#use with locator/joint based rig
#mirror selected locator(s)

import maya.cmds as cmds

sl = cmds.ls(sl=1)


for s in sl:
    name_selected = s
    name_changed = name_selected.replace("l_","r_")
    
    mirrorLoc = cmds.select(name_changed)
    mirrorTranslation = cmds.xform(mirrorLoc, t = True, query = True)
    mirrorRotation = cmds.xform(mirrorLoc, ro = True, query = True)
    
    translation = cmds.xform(s, t = True, query = True)
    rotation = cmds.xform(s, ro = True, query = True)

    cmds.xform(mirrorLoc, t = [-translation[0], translation[1], translation[2]], a= True)
    cmds.xform(mirrorLoc, ro = [rotation[0], -rotation[1], -rotation[2]], a= True)

    cmds.xform(s, t = [-mirrorTranslation[0], mirrorTranslation[1], mirrorTranslation[2]], a= True)
    cmds.xform(s, ro = [mirrorRotation[0], -mirrorRotation[1], -mirrorRotation[2]], a= True)
