import maya.cmds as cmds

def matrix_curl_connect(parent, targets=None, switch=None):
	if targets is None:
		targets = cmds.ls(sl = True)
	
	pm = parent + "_matrix_pm"
	if not cmds.objExists(pm):
		cmds.createNode("pickMatrix", name = pm)
		cmds.setAttr(pm + ".useTranslate", 0)
		cmds.setAttr(pm + ".useScale", 0)
		cmds.setAttr(pm + ".useShear", 0)
		cmds.connectAttr(parent + ".matrix", pm + ".inputMatrix")

	for target in targets:
		blendMatrix = cmds.createNode("blendMatrix", name = target + "_bm")
		# get offset matrix
		offset = cmds.getAttr(target + ".offsetParentMatrix")
		# set input matrix
		cmds.setAttr(blendMatrix + ".inputMatrix", offset, type = "matrix")
		# get connection from parent
		multMatrix = cmds.createNode("multMatrix", name = target + "_mm")
		cmds.connectAttr(pm + ".outputMatrix", multMatrix + ".matrixIn[0]")
		cmds.setAttr(multMatrix + ".matrixIn[1]", offset, type = "matrix")
		cmds.connectAttr(multMatrix + ".matrixSum", blendMatrix + ".target[0].targetMatrix")
		if switch:
			cmds.connectAttr(switch, blendMatrix + ".target[0].weight")
		else:
			cmds.setAttr(blendMatrix + ".target[0].weight", 1)
		cmds.connectAttr(blendMatrix + ".outputMatrix", target + ".offsetParentMatrix")

matrix_curl_connect("r_pnk_end_ctrl", targets=None, switch=None)