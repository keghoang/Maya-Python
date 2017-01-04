#connect similarly-named blendshapes from 2 rigs
#source's BS should be named: mocap_BS , target should be named: Ben_facial_BS

import maya.cmds as cmds

sl = cmds.ls(sl=1)
bs_list = cmds.listAttr('Ben_facial_BS.w', m = True)

for i in bs_list:
	cmds.connectAttr('mocap_BS.'+str(i), 'Ben_facial_BS.'+str(i), f = True)

#connectAttr -f mocap_BS.Eyes_Look_LeftShape Ben_facial_BS.Eyes_Look_LeftShape;