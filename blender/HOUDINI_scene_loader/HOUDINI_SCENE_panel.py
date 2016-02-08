import bpy
import math
import os
import sys
import xml.dom.minidom as dom
from bpy.app.handlers import persistent
#if os.path.dirname(bpy.data.filepath) not in sys.path:
#    sys.path.append(os.path.join(os.path.dirname(bpy.data.filepath),'python') )    
#import createMeshFromObjFile
#
#from bpy.app.handlers import persistent
### V2
class HoudiniSceneLoaderOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.houdini_scene_loader_operator"
    bl_label = "Load Houdini Scene"
    bl_context = "scene"

    

    def initData(self):  
        pass  
    
            
    def printInfos(self):
        print('infos !!!!')
    
    def loadShaders(self):
        D = bpy.data
        C = bpy.context


        filepath = "F:/PYTHON_playground/blender/HOUDINI_scene_loader/shaders/shaders_01.blend"
        # shaderName = "diffuseGlossyCustomShader"
        shaderName = ["diffuseGlossyCustomShader","diffuseGlossyTranslucentCustomShader","emissionCustomShader"]
        # append, set to true to keep the link to the original file
        link = False 



        # append all groups from the .blend file

        with bpy.data.libraries.load(filepath, link=link) as (data_src, data_dst):

            # print('hey', dir(data_src.objects[0]))
            # print('ho', data_src.materials[0])
            
            data_dst.node_groups = shaderName
            
            # bpy.data.node_groups.new(shaderName, 'ShaderNodeTree')



   


    def createShaders_V2(self, objName , shaderType, cyclesParamsDict):

        D = bpy.data
        C = bpy.context

        

        mat = D.materials.new(objName)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        D.objects[objName].data.materials.append(mat)

        if shaderType == 'emission':


            shaderName = "emissionCustomShader"
            groupNode = nodes.new('ShaderNodeGroup')
            groupNode.node_tree = bpy.data.node_groups[shaderName]   
            if cyclesParamsDict['use_point_color'] == 'on':
                groupNode.inputs['vertexColorMult'].default_value = 1.0
            else:
                groupNode.inputs['vertexColorMult'].default_value = 0.0

            groupNode.inputs['emissionStrength'].default_value = float(cyclesParamsDict['emissionStrength'])
            outputNode = nodes['Material Output']
            output = groupNode.outputs[0]
            input = outputNode.inputs[0]
            mat.node_tree.links.new(input, output)                          

        elif shaderType == 'diffuse+glossy':


            shaderName = "diffuseGlossyCustomShader"
            groupNode = nodes.new('ShaderNodeGroup')
            groupNode.node_tree = bpy.data.node_groups[shaderName]

            diffTexNode = nodes.new('ShaderNodeTexImage')
            diffTexNode.name = 'Diffuse Texture'
            diffTexNode.label = 'Diffuse Texture'
            if cyclesParamsDict['use_diffuse_texture'] == 'on':

                img = D.images.load(cyclesParamsDict['diffuse_texture'])
                groupNode.inputs['diffTextureMult'].default_value = 1.0
                diffTexNode.image = img
            else:
                groupNode.inputs['diffTextureMult'].default_value = 0.0

            

            groupNode.inputs["roughness"].default_value = float(cyclesParamsDict['roughness'])
            groupNode.inputs["diffuseColor"].default_value = (float(cyclesParamsDict['diffuseColorr']),float(cyclesParamsDict['diffuseColorg']), float(cyclesParamsDict['diffuseColorb']),1.0)
            groupNode.inputs["glossyColor"].default_value = (float(cyclesParamsDict['glossyColorr']),float(cyclesParamsDict['glossyColorg']), float(cyclesParamsDict['glossyColorb']),1.0)



            output = diffTexNode.outputs[0]
            input = groupNode.inputs['diffTexture']
            mat.node_tree.links.new(input, output)           

            if cyclesParamsDict['use_point_color'] == 'on':
                groupNode.inputs['vertexColorMult'].default_value = 1.0
            else:
                groupNode.inputs['vertexColorMult'].default_value = 0.0

       


            dispTexNode = nodes.new('ShaderNodeTexImage')
            dispTexNode.name = 'Displacement Texture'
            dispTexNode.label = 'Displacement Texture'
            if cyclesParamsDict['use_displacement'] == 'on':

                img = D.images.load(cyclesParamsDict['displacement_texture'])
                groupNode.inputs['displacementAmount'].default_value = float(cyclesParamsDict['displacementAmount'])
                dispTexNode.image = img
            else:
                groupNode.inputs['displacementAmount'].default_value = 0.0

            output = dispTexNode.outputs[0]
            input = groupNode.inputs['displacementTexture']
            mat.node_tree.links.new(input, output)                    

            outputNode = nodes['Material Output']
            output = groupNode.outputs[0]
            input = outputNode.inputs[0]
            mat.node_tree.links.new(input, output)    

            outputNode = nodes['Material Output']
            output = groupNode.outputs[1] ## displacement output
            input = outputNode.inputs[2]  ## displacement input
            mat.node_tree.links.new(input, output)    


        elif shaderType == 'diffuse+glossy+translucent':


            shaderName = "diffuseGlossyTranslucentCustomShader"
            groupNode = nodes.new('ShaderNodeGroup')
            groupNode.node_tree = bpy.data.node_groups[shaderName]

            diffTexNode = nodes.new('ShaderNodeTexImage')
            diffTexNode.name = 'Diffuse Texture'
            diffTexNode.label = 'Diffuse Texture'
            if cyclesParamsDict['use_diffuse_texture'] == 'on':

                img = D.images.load(cyclesParamsDict['diffuse_texture'])
                groupNode.inputs['diffTextureMult'].default_value = 1.0
                diffTexNode.image = img
            else:
                groupNode.inputs['diffTextureMult'].default_value = 0.0

            translucentTexNode = nodes.new('ShaderNodeTexImage')
            translucentTexNode.name = 'Diffuse Texture'
            translucentTexNode.label = 'Diffuse Texture'
            if cyclesParamsDict['use_diffuse_texture'] == 'on':

                img = D.images.load(cyclesParamsDict['diffuse_texture'])
                groupNode.inputs['diffTextureMult'].default_value = 1.0
                translucentTexNode.image = img
            else:
                groupNode.inputs['diffTextureMult'].default_value = 0.0            

            groupNode.inputs["roughness"].default_value = float(cyclesParamsDict['roughness'])
            groupNode.inputs["diffuseColor"].default_value = (float(cyclesParamsDict['diffuseColorr']),float(cyclesParamsDict['diffuseColorg']), float(cyclesParamsDict['diffuseColorb']),1.0)
            groupNode.inputs["glossyColor"].default_value = (float(cyclesParamsDict['glossyColorr']),float(cyclesParamsDict['glossyColorg']), float(cyclesParamsDict['glossyColorb']),1.0)
            groupNode.inputs["translucentColor"].default_value = (float(cyclesParamsDict['translucentColorr']),float(cyclesParamsDict['translucentColorg']), float(cyclesParamsDict['translucentColorb']),1.0)



            output = diffTexNode.outputs[0]
            input = groupNode.inputs['diffTexture']
            mat.node_tree.links.new(input, output)           

            output = translucentTexNode.outputs[0]
            input = groupNode.inputs['translucentTexture']
            mat.node_tree.links.new(input, output)                     

            if cyclesParamsDict['use_point_color'] == 'on':
                groupNode.inputs['vertexColorMult'].default_value = 1.0
            else:
                groupNode.inputs['vertexColorMult'].default_value = 0.0

       


            dispTexNode = nodes.new('ShaderNodeTexImage')
            dispTexNode.name = 'Displacement Texture'
            dispTexNode.label = 'Displacement Texture'
            if cyclesParamsDict['use_displacement'] == 'on':

                img = D.images.load(cyclesParamsDict['displacement_texture'])
                groupNode.inputs['displacementAmount'].default_value = float(cyclesParamsDict['displacementAmount'])
                dispTexNode.image = img
            else:
                groupNode.inputs['displacementAmount'].default_value = 0.0

            output = dispTexNode.outputs[0]
            input = groupNode.inputs['displacementTexture']
            mat.node_tree.links.new(input, output)                    

            outputNode = nodes['Material Output']
            output = groupNode.outputs[0]
            input = outputNode.inputs[0]
            mat.node_tree.links.new(input, output)    

            outputNode = nodes['Material Output']
            output = groupNode.outputs[1] ## displacement output
            input = outputNode.inputs[2]  ## displacement input
            mat.node_tree.links.new(input, output)    

        

    def loadXMLData(self, xmlFile):
        # print('loadXMLData function -------')
        xmlData = dom.parse(xmlFile)
        camList = xmlData.firstChild.getElementsByTagName('camera')
        objList = xmlData.firstChild.getElementsByTagName('object')
        
        SHADERS_LOADED = False

        # imports cams
        for cam in camList:

            camName = cam.getAttribute('name')
            
            try : 
                candidate = bpy.context.scene.objects[camName]

                bpy.ops.object.select_all(action='DESELECT')
                candidate.select = True
                print (candidate.name, "delete -----------------")
                bpy.ops.object.delete()
                bpy.ops.object.select_all(action='DESELECT')
            except:
                pass                     
            
            
            
            focalLength = float(cam.getAttribute('focal_length'))
            aperture = float(cam.getAttribute('aperture'))
            focusDistance = float(cam.getAttribute('focus_distance'))
            fstop = float(cam.getAttribute('fstop'))
            


            confPath = bpy.context.scene.conf_path
            projectDir = os.path.split(confPath)[0]

            fbxFilePath = '%s/geo/%s.fbx' % (projectDir,camName)
            bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, anim_offset=1)          
            
            camObj =  bpy.context.scene.objects[camName] 
            camCam = bpy.data.cameras[camName]
            
            camCam.cycles.aperture_type = "FSTOP"
            camCam.cycles.aperture_fstop = fstop
            
       


            camObj.data.lens = focalLength
            camObj.data.sensor_width = aperture
            camObj.data.dof_distance = focusDistance            
            
            animatedParams = cam.getElementsByTagName('animatedParams')[0]
            for param in animatedParams.getElementsByTagName('param'):
                # print(dir(param))
                if param.getAttribute('name') == 'focus':
                    strValues = param.getAttribute('values').strip(',[]').split(',')
                    for i, val in enumerate(strValues):
                        camCam.dof_distance = float(val)
                        camCam.keyframe_insert(data_path='dof_distance', frame=i+2)

                if param.getAttribute('name') == 'aperture':
                    strValues = param.getAttribute('values').strip(',[]').split(',')
                    for i, val in enumerate(strValues):
                        camCam.sensor_width = float(val)
                        camCam.keyframe_insert(data_path='sensor_width', frame=i+2)           

                if param.getAttribute('name') == 'focal':
                    strValues = param.getAttribute('values').strip(',[]').split(',')
                    for i, val in enumerate(strValues):
                        camCam.lens = float(val)
                        camCam.keyframe_insert(data_path='lens', frame=i+2)                 

                if param.getAttribute('name') == 'fstop':
                    strValues = param.getAttribute('values').strip(',[]').split(',')
                    for i, val in enumerate(strValues):
                        camCam.cycles.aperture_fstop = float(val)
                        camCam.keyframe_insert(data_path='cycles.aperture_fstop', frame=i+2)                                                         



        objSequences = {}
        
        #### import  objects
        for obj in objList:


            objName = obj.getAttribute('name')
            shaderName = obj.getAttribute('shaderName')
            animationType = obj.getAttribute('animationType')
            shaderType = obj.getAttribute('shaderType')    

            cyclesParams = obj.getElementsByTagName('cyclesParams')        
            cyclesParamsDict = {}
            for child in cyclesParams[0].childNodes:
                if child.nodeType == 1: ######### ???
                    cyclesParamsDict[child.nodeName] = child.getAttribute('value')
            
            # print(cyclesParamsDict)        


            try : 
                candidate = bpy.data.objects[objName]

                bpy.ops.object.select_all(action='DESELECT')
                candidate.select = True
                print (candidate.name, "delete -----------------")
                bpy.ops.object.delete()
                bpy.ops.object.select_all(action='DESELECT')
                
            except:
                pass                
            

            isPointAnim = obj.getAttribute('isPointAnim') == 'True'

  
            ### import fbx
            if animationType == 'mesh_cache' or not isPointAnim:
                fbxFilePath = '%s/geo/%s.fbx' % (projectDir, objName)
                bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100)
            else:
                # print("load file path current frame")
                fbxFilePath = '%s/geo/%s_sequence/%s_1.fbx' % (projectDir, objName, objName)
                bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100)
            
            if isPointAnim and animationType == 'mesh_cache':
                bpy.context.scene.objects[objName].modifiers.new('mesh_cache','MESH_CACHE')
                mod = bpy.context.scene.objects[objName].modifiers['mesh_cache']
                mod.cache_format = 'PC2'
                mod.frame_start = 1.0
                
                pc2File = obj.getElementsByTagName('pc2file')[0]
                pc2FilePath = pc2File.getAttribute('filepath')
                
                mod.filepath = pc2FilePath

            ### import fbx sequence
            elif isPointAnim and animationType == 'fbx_sequence':
                ##### load fbx file according to current frame in a frame_change_pre callback function')
                fbxFrames = obj.getElementsByTagName('fbxFrame')
                framesDict = {}
                for frame in fbxFrames:
                    frameNumber = int(frame.getAttribute('frameNumber'))
                    filePath = frame.getAttribute('filePath')
                    framesDict[frameNumber] = filePath
                objSequences[objName] = framesDict





                
            fbxObj = bpy.context.scene.objects[objName]
            fbxObj.data.use_auto_smooth = False



            fbxObj.cycles_visibility.camera = int(cyclesParamsDict['rayVisCamera'] == 'on')
            fbxObj.cycles_visibility.diffuse = int(cyclesParamsDict['rayVisDiffuse'] == 'on')
            fbxObj.cycles_visibility.glossy = int(cyclesParamsDict['rayVisGlossy'] == 'on')
            fbxObj.cycles_visibility.transmission = int(cyclesParamsDict['rayVisTransmission'] == 'on')
            fbxObj.cycles_visibility.scatter = int(cyclesParamsDict['rayVisVolumeScatter'] == 'on')
            fbxObj.cycles_visibility.shadow = int(cyclesParamsDict['rayVisShadow'] == 'on')
            try:
                if len(fbxObj.data.materials) != 0:
                    fbxObj.data.materials[0] = bpy.data.materials[shaderName]
                else:    
                    fbxObj.data.materials.append(bpy.data.materials[shaderName])
            except:
                pass

            
            self.createShaders_V2(objName, shaderType, cyclesParamsDict)   
      



        #### define callback method
        @persistent
        def callbackFunction(self):

            # remove meshes with no users
            for mesh in bpy.data.meshes:
                if mesh.users == 0:
                    bpy.data.meshes.remove(mesh)            

            frame_current  = bpy.context.scene.frame_current

            print (len(objSequences))
            for objName in objSequences:
                try:
                    fbxFilePath = objSequences[objName][frame_current]
                except:
                    return


                # print(fbxFilePath, '::')
                ##deselect all
                bpy.ops.object.select_all(action='DESELECT')
                
                ##delete old geometry
                bpy.ops.object.select_pattern(pattern=objName)
                bpy.ops.object.delete(use_global=False)

                ##### import current frame geometry
                currentFrameObj = bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100)
                # currentFrameObj.name = objName    
                fbxObj = bpy.context.scene.objects[objName]
                fbxObj.data.use_auto_smooth = False     
                try:
                    if len(fbxObj.data.materials) != 0:
                        fbxObj.data.materials[0] = bpy.data.materials[objName]
                    else:    
                        fbxObj.data.materials.append(bpy.data.materials[objName])
                except:
                    pass                           
                    
        bpy.app.handlers.frame_change_pre.append(callbackFunction )
        # bpy.app.handlers.render_pre.append(callbackFunction )


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # self.report({'INFO'}, "Loading Houdini XML custom Scene File")
        self.initData()
        self.printInfos()
        self.loadShaders()
        self.loadXMLData(bpy.context.scene.conf_path)
        return {'FINISHED'}

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Houdini Scene"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"


#    @persistent
    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")
    
        row = layout.row()


        row.prop(context.scene, 'conf_path')
        row.prop(context.scene, 'fbxSequences')
        
        row = layout.row()


        # Big render button

        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.houdini_scene_loader_operator")




def register():
    bpy.utils.register_class(HoudiniSceneLoaderOperator)   
    bpy.utils.register_class(LayoutDemoPanel)

    bpy.types.Scene.conf_path = bpy.props.StringProperty \
      (
      name = "Root Path",
      default = "",
      description = "XML file describing content of the scene",
      subtype = 'FILE_PATH'
      )    
     
    bpy.types.Scene.fbxSequences = bpy.props.StringProperty \
      (
      name = "fbx Sequences",
      default = "",
      description = "list of fbx sequences in the xml scene file",
      subtype = 'FILE_PATH'
      )  

def unregister():
    bpy.utils.unregister_class(HoudiniSceneLoaderOperator)
    bpy.utils.unregister_class(LayoutDemoPanel)
    del bpy.types.Scene.conf_path
    del bpy.types.Scene.fbxSequences
    


if __name__ == "__main__":
    register()


print('HOUDINI_SCENE_LOADER_V2')