import bpy
import sys
import os
#from sys import stdout



D = bpy.data
C = bpy.context
sceneFilePath = sys.argv[-3] # start from the end: these are 'trailing' parameters to the command blender.exe and its parameters
DO_RENDER = int(sys.argv[-2])
parmsDict = sys.argv[-1]



dictString = parmsDict.split(',')
print(dictString)

goodParmsDict = {}
for s in dictString:
    # print (s.split(':')[0].strip(' '), s.split(':')[1].strip(' '))
    key = s.split(':')[0].strip(' ,\'{}')
    value = s.split(':')[1].strip('\'}{ ')
    goodParmsDict[key] = value    
    


scene = D.scenes['Scene']
bpy.context.scene.conf_path = sceneFilePath

print(sceneFilePath, " ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

C.scene.render.engine = 'CYCLES'

# override = {'screen': bpy.context.screen}
# bpy.ops.script.python_file_run(override,filepath="C:\\Program Files\\Blender Foundation\\Blender\\2.76\\scripts\\presets\\framerate\\25.py")


scene.cycles.device = goodParmsDict['device']
scene.cycles.use_square_samples = True
scene.cycles.samples = int(goodParmsDict['samples'])
scene.cycles.film_transparent = goodParmsDict['transparent'] == 'True'
scene.cycles.film_exposure = float(goodParmsDict['filmExposure'])
scene.cycles.blur_glossy = float(goodParmsDict['blurGlossy'])
scene.cycles.use_animated_seed = True

if goodParmsDict['experimental'] == 'True':

	scene.cycles.feature_set = 'EXPERIMENTAL'
else:
	scene.cycles.feature_set = 'SUPPORTED'

scene.render.resolution_x = int(goodParmsDict['resolutionX'])
scene.render.resolution_y = int(goodParmsDict['resolutionY'])
scene.render.resolution_percentage = int(goodParmsDict['resolutionPercentage'])

scene.render.tile_x =  int(goodParmsDict['tileSize'])
scene.render.tile_y =  int(goodParmsDict['tileSize'])


scene.render.use_motion_blur = goodParmsDict['useMotionBlur'] == 'True'

### set background Shader
D.worlds['World'].use_nodes = True
D.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (0.0,0.0,0.0,1.0)



### limitedd global illumination

cycles = bpy.context.scene.cycles

cycles.max_bounces = 8
cycles.min_bounces = 3
cycles.caustics_reflective = False
cycles.caustics_refractive = False
cycles.diffuse_bounces = 3
cycles.glossy_bounces = 4
cycles.transmission_bounces = 8


doVolumePass = goodParmsDict['volumePass'] == 'True'
if doVolumePass :
	cycles.volume_bounces = 0
else:
	cycles.volume_bounces = 2

cycles.transparent_min_bounces = 8
cycles.transparent_max_bounces = 16

### HOUDINI scene loader
bpy.ops.object.houdini_scene_loader_operator()
### don't need it, fps is probably set by fbx importer
# C.scene.render.fps = 25.0

outputPath = goodParmsDict['outputPath']

galere = outputPath[:1]+ ':' + outputPath[1:] 

ext = galere.split('.')[-1:][0]
if ext == 'exr' or ext =='EXR' :
	
	scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
	scene.render.image_settings.color_depth = '32'
	scene.render.layers['RenderLayer'].use_pass_mist = True


	scene.render.layers['RenderLayer'].use_pass_diffuse_color = True
	scene.render.layers['RenderLayer'].use_pass_diffuse_direct = True
	scene.render.layers['RenderLayer'].use_pass_diffuse_indirect = True

	scene.render.layers["RenderLayer"].use_pass_glossy_color = True
	scene.render.layers["RenderLayer"].use_pass_glossy_direct = True
	scene.render.layers["RenderLayer"].use_pass_glossy_indirect = True

	scene.render.layers["RenderLayer"].use_pass_transmission_color = True
	scene.render.layers["RenderLayer"].use_pass_transmission_direct = True
	scene.render.layers["RenderLayer"].use_pass_transmission_indirect = True

	scene.render.layers["RenderLayer"].use_pass_emit = True



elif ext =='png' or ext == 'PNG' :
	scene.render.image_settings.file_format = 'PNG'
	scene.render.image_settings.color_depth = '16'
elif ext =='tga' or ext == 'TGA' :
	scene.render.image_settings.file_format = 'TARGA'	
	# scene.render.image_settings.color_depth = '16'
else:
	##default to PNG
	scene.render.image_settings.file_format = 'PNG'
	scene.render.image_settings.color_depth = '16'

extLength = len(ext)
print ("Saved: -->",galere)


# sp = outputPath.split('/')

# goodPath =os.path.join(*sp)

if doVolumePass :
	C.scene.render.filepath = galere[:-4]+'_volume'
else:
	C.scene.render.filepath = galere[:-4]


scene.render.use_file_extension =  True

fStart = int(goodParmsDict['fStart'])
fEnd = int(goodParmsDict['fEnd'])
if DO_RENDER:
	for i in range(fStart,fEnd+1):
		C.scene.frame_current = i

		


		if doVolumePass :
			C.scene.render.filepath = galere[:-4]+'_volume_'+str(i)
		else:
			C.scene.render.filepath = galere[:-4]+'_'+str(i)
		scene.camera = bpy.data.objects['export_cam1']

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