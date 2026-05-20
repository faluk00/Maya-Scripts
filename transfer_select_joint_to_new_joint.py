import maya.cmds as cmds

def transfer_skin(mesh, jnt, new_jnt):
	# get vertex count
	vertex_count = cmds.getAttr(mesh+".vtx[*]")
	# get mesh shape
	mesh_shapes = cmds.listRelatives(
		mesh,
		shapes=True
	)
	# get connected skin cluster
	skin_cluster = cmds.listConnections(
		mesh_shapes[0],
		type="skinCluster"
	)
	# if this mesh isn't bind skin yet then return None
	if not skin_cluster:
		print("No skin cluster")
		print(mesh_shapes[0])
		return None
	# check is new joint already bond
	inf_jnts = cmds.skinCluster(mesh, q=True, influence=True)
	if new_jnt not in inf_jnts:
		cmds.skinCluster(mesh, e=True, addInfluence=new_jnt, weight=0, lockWeights=False)
	
	mesh_data = {
		"name": mesh,
		"vertex_count": len(vertex_count),
		"skin_cluster": skin_cluster[0],
	}
	
	vertex = []
	
	for i in range(len(vertex_count)):
		# get vertex name
		vtx = "{0}.vtx[{1}]".format(mesh, str(i))
		# get position
		position = cmds.xform(
			vtx,
			q = True,
			ws = True,
			t = True
		)
		# get vertex skin percent
		skin_percent = cmds.skinPercent(
			skin_cluster[0],
			vtx,
			q = True,
			value = True
		)
		# get influence joints
		influence_joints = cmds.skinPercent(
			skin_cluster[0],
			vtx,
			q = True,
			transform = None
		)
		# print(skin_percent)
		# match skin data
		for n in range(len(skin_percent)):
			
			if influence_joints[n] == jnt and skin_percent[n] > 0:
				print(vtx)
				# remove old jnt
				skin_data = [jnt, 0.0]
				cmds.skinPercent(
					skin_cluster[0],
					vtx,
					transformValue = skin_data
				)
				# set new jnt
				skin_data = [new_jnt, skin_percent[n]]
				print(skin_data)
				cmds.skinPercent(
					skin_cluster[0],
					vtx,
					transformValue = skin_data
				)

# transfer_skin(mesh = "FruitGirl_hair", jnt = "head_jnt", new_jnt = "head_up_jnt")