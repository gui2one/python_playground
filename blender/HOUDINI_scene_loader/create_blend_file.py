import bpy
import time
import sys
import os
cmdArg = sys.argv[-1]
fbxFilePath = cmdArg
# print ('{gui2one_INFOS:}', fbxFilePath)


### delete all objects in the scene before anything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, use_image_search=False)
# time.sleep(5)

bpy.ops.wm.save_mainfile(filepath= fbxFilePath[:-4]+'.blend')
print("create blend file", bpy)


class createBlendFile:

    def __init__(self):

    	
        self.my_func()
        self.loadShaders()

    def loadShaders(self):
        D = bpy.data
        C = bpy.context

        PYTHON_PLAYGROUND = os.getenv('PYTHON_PLAYGROUND')
        if not PYTHON_PLAYGROUND:
            print('ERROR : PYTHON_PLAYGROUND env variables NOT set')
            sys.exit(0)
        filepath = PYTHON_PLAYGROUND+"/blender/HOUDINI_scene_loader/shaders/shaders_01.blend"
        # shaderName = "diffuseGlossyCustomShader"
        shaderName = ["diffuseGlossyCustomShader","diffuseGlossyTranslucentCustomShader","diffuseAnisotropicCustomShader","emissionCustomShader"]
        # append, set to true to keep the link to the original file
        link = False 



        # append all groups from the .blend file

        with bpy.data.libraries.load(filepath, link=link) as (data_src, data_dst):

            # print('hey', dir(data_src.objects[0]))
            # print('ho', data_src.materials[0])
            
            data_dst.node_groups = shaderName
            
            # bpy.data.node_groups.new(shaderName, 'ShaderNodeTree')

        print('{gui2one_INFOS:} what ???????????????')



    def my_func(self):

        pass
    	


if __name__ == "__main__":
		x = createBlendFile()



# bpy.ops.wm.quit_blender()
