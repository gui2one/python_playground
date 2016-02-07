import bpy
import sys
#from sys import stdout



D = bpy.data
C = bpy.context
sceneFilePath = sys.argv[-2] # start from the end: these are 'trailing' parameters to the command blender.exe and ITS parameters
DO_RENDER = int(sys.argv[-1])



bpy.context.scene.conf_path = sceneFilePath

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

C.scene.render.engine = 'CYCLES'

# override = {'screen': bpy.context.screen}
# bpy.ops.script.python_file_run(override,filepath="C:\\Program Files\\Blender Foundation\\Blender\\2.76\\scripts\\presets\\framerate\\25.py")


D.scenes['Scene'].cycles.device = 'GPU'
D.scenes['Scene'].cycles.use_square_samples = True
D.scenes['Scene'].cycles.samples = 28
D.scenes['Scene'].cycles.film_transparent = True


D.scenes['Scene'].render.resolution_percentage = 75

D.scenes['Scene'].render.tile_x = 128
D.scenes['Scene'].render.tile_y = 128

D.scenes['Scene'].render.use_motion_blur = True

### set background Shader
D.worlds['World'].use_nodes = True
D.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (0.0,0.0,0.0,1.0)


### HOUDINI scene loader
bpy.ops.object.houdini_scene_loader_operator()
### don't need it, fps is probably set by fbx importer
# C.scene.render.fps = 25.0
fStart = 1
fEnd = 229
if DO_RENDER:
	for i in range(fStart,fEnd+1):
		C.scene.frame_current = i
		C.scene.render.filepath = "F:/BLENDER_playground/render/world/world_%s.png" % i
		D.scenes['Scene'].camera = bpy.data.objects['export_cam1']

		### render
		bpy.ops.render.render(write_still=True)
 

		# print("rendered frame %s \r" % (i))
		#stdout.write("rendered frame %d\n" % i)

	# remove meshes with no users
	for mesh in D.meshes:
		if mesh.users == 0:
			D.meshes.remove(mesh)

		print("rendered frame %s" % i)







print('------------- launch script ENDED ---------------')

# bpy.ops.wm.quit_blender()