import bpy
import sys


print (sys.argv[4], ':::::::::::')
bpy.context.scene.conf_path = sys.argv[4]

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))



bpy.ops.scene.houdini_scene_loader_operator()
bpy.context.scene.render.filepath = "F:/BLENDER_playground/test.png"

bpy.data.scenes['Scene'].camera = bpy.data.objects['export_cam1']
bpy.context.scene.render.engine = 'CYCLES'
 
# render
bpy.ops.render.render(write_still=True)
 






print('------------- launch script ENDED ---------------')

bpy.ops.wm.quit_blender()