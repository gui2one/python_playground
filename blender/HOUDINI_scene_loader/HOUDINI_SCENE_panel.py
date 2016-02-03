import bpy
import math
import os
import sys
import xml.dom.minidom as dom
#if os.path.dirname(bpy.data.filepath) not in sys.path:
#    sys.path.append(os.path.join(os.path.dirname(bpy.data.filepath),'python') )    
#import createMeshFromObjFile
#
#from bpy.app.handlers import persistent
### V2
class HoudiniSceneLoaderOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.houdini_scene_loader_operator"
    bl_label = "Load Houdini Scene"
    bl_context = "scene"


    def initData(self):  
        pass  
    
            
    def printInfos(self):
        print('infos !!!!')
        
    def createShader(self, shaderName, shaderType):
        print("create shader", shaderName)
        C = bpy.context
        D = bpy.data

        for mat in D.materials:
            if mat.users == 0:
                D.materials.remove(mat)

        mats = D.materials        

        if(shaderType == 'diffuse+glossy'):

            newMat = D.materials.new(name=shaderName)
            newMat.use_nodes = True

            pos_x = 1200
            pos_y = 300
            nodes = newMat.node_tree.nodes

            outputNode = nodes['Material Output']
            outputNode.location = pos_x, pos_y

            pos_x += -200

            addNode = nodes.new('ShaderNodeAddShader')
            addNode.name = 'Mix Shader'
            addNode.location = pos_x, pos_y



            pos_x += -300
            pos_y += 150
            glossyNode = nodes.new('ShaderNodeBsdfGlossy')
            glossyNode.name = 'Glossy BSDF'
            glossyNode.location = pos_x, pos_y
            glossyNode.inputs['Roughness'].default_value = 0.05

            pos_x += -200
            fresnelNode = nodes.new('ShaderNodeFresnel')
            fresnelNode.location = pos_x, pos_y



            pos_y += -300
            pos_x += 200
            diffuseNode = nodes['Diffuse BSDF']
            diffuseNode.location = pos_x, pos_y



            pos_x += -200
            diffRGBNode = nodes.new('ShaderNodeRGB')
            diffRGBNode.location = pos_x, pos_y

            output = addNode.outputs[0]
            input = outputNode.inputs['Surface']
            newMat.node_tree.links.new(input, output)

            output = glossyNode.outputs[0]
            input = addNode.inputs[0]
            newMat.node_tree.links.new(input, output)



            output = diffuseNode.outputs[0]
            input = addNode.inputs[1]
            newMat.node_tree.links.new(input, output)


            output = fresnelNode.outputs[0]
            input = glossyNode.inputs[0]
            newMat.node_tree.links.new(input, output)



            output = diffRGBNode.outputs[0]
            input = diffuseNode.inputs[0]
            newMat.node_tree.links.new(input, output)        


        if(shaderType == 'emission'):
            newMat = D.materials.new(name=shaderName)
            newMat.use_nodes = True

            pos_x = 1200
            pos_y = 300
            nodes = newMat.node_tree.nodes

            outputNode = nodes['Material Output']
            outputNode.location = pos_x, pos_y

            pos_x += -200

            emissionNode = nodes.new('ShaderNodeEmission')

            emissionNode.location = pos_x, pos_y
            emissionNode.inputs['Strength'].default_value = 10.0

            output = emissionNode.outputs[0]
            input = outputNode.inputs['Surface']
            newMat.node_tree.links.new(input, output)            




    def loadXMLData(self, xmlFile):
        print('loadXMLData function -------')
        xmlData = dom.parse(xmlFile)
        camList = xmlData.firstChild.getElementsByTagName('camera')
        objList = xmlData.firstChild.getElementsByTagName('object')
        

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
            
            posList = cam.getElementsByTagName('translation')[0].firstChild.wholeText.split(' ')
            rotList = cam.getElementsByTagName('rotation')[0].firstChild.wholeText.split(' ')

            confPath = bpy.context.scene.conf_path
            projectDir = os.path.split(confPath)[0]

            fbxFilePath = '%s/geo/%s.fbx' % (projectDir,camName)
            bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, anim_offset=0)          
            
            camObj =  bpy.context.scene.objects[camName] 
            camCam = bpy.data.cameras[camName]
            

            
            # camObj.location.x = float(posList[0])           
            # camObj.location.y = float(posList[2]) *-1           
            # camObj.location.z = float(posList[1])     
            


            camObj.data.lens = focalLength
            camObj.data.sensor_width = aperture
            camObj.data.dof_distance = focusDistance            
            
            


        
        
        #### import  objects
        for obj in objList:


            objName = obj.getAttribute('name')
            shaderName = obj.getAttribute('shaderName')
            animationType = obj.getAttribute('animationType')
            shaderType = obj.getAttribute('shaderType')            

            self.createShader(objName, shaderType)
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
                print("load file path current frame")
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
            elif isPointAnim and animationType == 'fbx_sequence':
                print('TODO : load fbx file according to current frame in a frame_change_pre callback function')

                def callbackFunction(self):
                    print(bpy.context.scene.frame_current)

                bpy.app.handlers.frame_change_pre.append(callbackFunction )
            fbxObj = bpy.context.scene.objects[objName]
            fbxObj.data.use_auto_smooth = False
            try:
                if len(fbxObj.data.materials) != 0:
                    fbxObj.data.materials[0] = bpy.data.materials[shaderName]
                else:    
                    fbxObj.data.materials.append(bpy.data.materials[shaderName])
            except:
                pass
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.report({'INFO'}, "Loading Houdini XML custom Scene File")
        self.initData()
        self.printInfos()
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
        row.operator("scene.houdini_scene_loader_operator")




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