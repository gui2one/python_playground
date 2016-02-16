import bpy
import time
print("create blend file", bpy)

fbxFilePath = 'F:/HOUDINI_15_playground/geo/box.fbx'
bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, use_image_search=False)
# time.sleep(5)
print("create blend file", bpy)
# bpy.ops.wm.quit_blender()