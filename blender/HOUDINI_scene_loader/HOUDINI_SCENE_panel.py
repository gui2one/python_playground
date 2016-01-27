import bpy
import math
import os
import sys
import xml.dom.minidom as dom
if os.path.dirname(bpy.data.filepath) not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(bpy.data.filepath),'python') )    
import createMeshFromObjFile


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Load Houdini Scene"
    bl_context = "scene"


    def initData(self):  
        pass  
    
            
    def printInfos(self):
        print('infos !!!!')
        
        
    def loadXMLData(self, xmlFile):
        print('loadXMLData function -------')
        xmlData = dom.parse(xmlFile)
        camList = xmlData.firstChild.getElementsByTagName('camera')
        objList = xmlData.firstChild.getElementsByTagName('object')
        
        for cam in camList:
#            print ("\n--------------------------")
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
#            camObj = bpy.data.objects.new(camName,camCam)
            fbxFilePath = '%s/geo/%s.fbx' % (projectDir,camName)
            bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100)          
            
            camObj =  bpy.context.scene.objects[camName] 
            camCam = bpy.data.cameras[camName]
            #bpy.context.scene.objects.link(camObj)
            

#            createMeshFromObjFile.createMeshFromObjFile('F:/BLENDER_playground/houdini_hips/geo/geo1.obj')  
            
#            camObj.rotation_euler.x = (float(rotList[0])+90)*(pi/180.0)
            camObj.rotation_euler.x = math.radians(float(rotList[0])+90)
            camObj.rotation_euler.y = math.radians(float(rotList[2]))           
            camObj.rotation_euler.z = math.radians(float(rotList[1]))    
            
            camObj.location.x = float(posList[0])           
            camObj.location.y = float(posList[2]) *-1           
            camObj.location.z = float(posList[1])     
            
#            fbxObj.data.use_auto_smooth = False       

            camObj.data.lens = focalLength
            camObj.data.sensor_width = aperture
            camObj.data.dof_distance = focusDistance            
            
            
#            print ("--------------------------\n")

        
        
        #### import  objects
        for obj in objList:
            objName = obj.getAttribute('name')
            shaderName = obj.getAttribute('shaderName')
            
            try : 
                candidate = bpy.data.objects[objName]

                bpy.ops.object.select_all(action='DESELECT')
                candidate.select = True
                print (candidate.name, "delete -----------------")
                bpy.ops.object.delete()
                bpy.ops.object.select_all(action='DESELECT')
                
            except:
                pass                
              
            fbxFilePath = '%s/geo/%s.fbx' % (projectDir, objName)
            bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100)
            isPointAnim = obj.getAttribute('isPointAnim') == 'True'
            if isPointAnim :
                bpy.context.scene.objects[objName].modifiers.new('mesh_cache','MESH_CACHE')
                mod = bpy.context.scene.objects[objName].modifiers['mesh_cache']
                mod.cache_format = 'PC2'
                
                pc2File = obj.getElementsByTagName('pc2file')[0]
                pc2FilePath = pc2File.getAttribute('filepath')
                
                mod.filepath = pc2FilePath
            
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
        self.report({'INFO'}, "Button clicked!")
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


        
    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")
    
        row = layout.row()


        row.prop(context.scene, 'conf_path')
        
        row = layout.row()




        # Big render button

        row = layout.row()
        row.scale_y = 3.0
        row.operator("object.simple_operator")

        
#        # Different sizes in a row
#        layout.label(text="Different button sizes:")
#        row = layout.row(align=True)
#        row.operator("render.render")
#
#
#        row.operator("render.render")


def register():
    bpy.utils.register_class(SimpleOperator)   
    bpy.utils.register_class(LayoutDemoPanel)

    bpy.types.Scene.conf_path = bpy.props.StringProperty \
      (
      name = "Root Path",
      default = "",
      description = "XML file describing content of the scene",
      subtype = 'FILE_PATH'
      )    
     


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(LayoutDemoPanel)
    del bpy.types.Scene.conf_path
    


if __name__ == "__main__":
    register()
