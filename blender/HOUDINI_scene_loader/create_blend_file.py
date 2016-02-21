import bpy
import time
import sys
import os
import xml.dom.minidom as dom
fbxFilePath = sys.argv[-3]
xmlFilePath = sys.argv[-2]
isLast = sys.argv[-1] == 'True'

# print ('{gui2one_INFOS:}', fbxFilePath)

D = bpy.data
C = bpy.context
### delete all objects in the scene before anything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

C.scene.render.engine = 'CYCLES'
bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, use_image_search=False)
# time.sleep(5)




class createBlendFile:

    def __init__(self):

    	

        self.loadShaders()
        self.createShaders(xmlFilePath)

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

        



    def createShaders(self, xmlFile):

        D = bpy.data
        C = bpy.context

        ## clean materials with no users
        mats = D.materials
        for mat in mats:
            if mat.users == 0:
                D.materials.remove(mat)

        ## not an error : relist materials
        mats = D.materials
        for mat in mats:
            if '.' in mat.name:
                mat.name = mat.name.split('.')[0]

        ### if materials with '.001' remains, they are duplicates, so replace this material with the source one
        ### again :
        for obj in D.objects:
            # print ("material_slot -->",obj.material_slots.__len__())
            for slot in obj.material_slots:
                if '.' in slot.material.name:
                    slot.material = D.materials[ slot.material.name.split('.')[0] ]

        ## clean materials with no users one last time
        mats = D.materials
        for mat in mats:
            if mat.users == 0:
                D.materials.remove(mat)       


        ### now that we have cleaned up the scene of bad duplicate materials 
        ### now load materials from xml file
        xmlData = dom.parse(xmlFile)

        
        materialList = xmlData.firstChild.getElementsByTagName('material')
        for material in materialList:
            materialName = material.getAttribute('name')
            cyclesParamsDict = {}
            for child in material.childNodes:
                if child.nodeType == 1:
                    cyclesParamsDict[child.nodeName] = child.getAttribute('value')

            print ('---------------------------')
            

            self.initShader(materialName,cyclesParamsDict['shader_type'], cyclesParamsDict )     


            # print (material.getAttribute('name'),  "--->", material.childNodes)
        

        ## now good materials were created, but they still don't have the right name ( e.g they have '.001' at the end)

        for obj in D.objects:
            # print ("material_slot -->",obj.material_slots.__len__())
            for slot in obj.material_slots:               
                slot.material = D.materials[ slot.material.name.split('.')[0]+'.001' ]

        ## finally : reclean materials with no users
        mats = D.materials
        for mat in mats:
            if mat.users == 0:
                D.materials.remove(mat)

        ## and rename them whitout '.001'
        mats = D.materials
        for mat in mats:
            if '.' in mat.name:
                mat.name = mat.name.split('.')[0]


        


    def initShader(self, objName , shaderType, cyclesParamsDict):

        D = bpy.data
        C = bpy.context

        

        mat = D.materials.new(objName)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        # if len(D.objects[objName].data.materials) == 0:
        #     D.objects[objName].data.materials.append(mat)
        # else :
        #     D.objects[objName].data.materials[0] = mat


        if shaderType == 'emission':


            shaderName = "emissionCustomShader"
            groupNode = nodes.new('ShaderNodeGroup')
            groupNode.node_tree = bpy.data.node_groups[shaderName]   
            if cyclesParamsDict['use_point_color'] == 'on':
                groupNode.inputs['vertexColorMult'].default_value = 1.0
            else:
                groupNode.inputs['vertexColorMult'].default_value = 0.0

            diffTexNode = nodes.new('ShaderNodeTexImage')
            diffTexNode.name = 'Emission Texture'
            diffTexNode.label = 'Emission Texture'
            if cyclesParamsDict['use_diffuse_texture'] == 'on':
                if cyclesParamsDict['diffuse_texture'] != '':
                    img = D.images.load(cyclesParamsDict['diffuse_texture'])
 
                    diffTexNode.image = img

                    output = diffTexNode.outputs['Color']
                    input = groupNode.inputs['emissionColor']
                    mat.node_tree.links.new(input, output)                          
   




            ## set emission color to diffuse color
            groupNode.inputs['emissionColor'].default_value = (float(cyclesParamsDict['diffuse_colorr']),float(cyclesParamsDict['diffuse_colorg']), float(cyclesParamsDict['diffuse_colorb']),1.0)
            groupNode.inputs['emissionStrength'].default_value = float(cyclesParamsDict['emission_strength'])
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
                if cyclesParamsDict['diffuse_texture'] != '':
                    img = D.images.load(cyclesParamsDict['diffuse_texture'])
                    groupNode.inputs['diffTextureMult'].default_value = 1.0
                    diffTexNode.image = img
            else:
                groupNode.inputs['diffTextureMult'].default_value = 0.0

            

            groupNode.inputs["roughness"].default_value = float(cyclesParamsDict['roughness'])
            groupNode.inputs["diffuseColor"].default_value = (float(cyclesParamsDict['diffuse_colorr']),float(cyclesParamsDict['diffuse_colorg']), float(cyclesParamsDict['diffuse_colorb']),1.0)
            groupNode.inputs["glossyColor"].default_value = (float(cyclesParamsDict['glossy_colorr']),float(cyclesParamsDict['glossy_colorg']), float(cyclesParamsDict['glossy_colorb']),1.0)
            groupNode.inputs["fresnelMult"].default_value = float(cyclesParamsDict['fresnel_mult'])

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
                groupNode.inputs['displacementAmount'].default_value = float(cyclesParamsDict['displacement_amount'])
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

        elif shaderType == 'diffuse+anisotropic':


            shaderName = "diffuseAnisotropicCustomShader"
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

            
            output = diffTexNode.outputs[0]
            input = groupNode.inputs['diffTexture']
            mat.node_tree.links.new(input, output)     


            ### anisotropy texture

            if cyclesParamsDict['use_anisotropy_texture'] == 'on':

                anisoTexNode = nodes.new('ShaderNodeTexImage')
                anisoTexNode.name = 'Anisotropy Texture'
                anisoTexNode.label = 'Anisotropy Texture'

                img = D.images.load(cyclesParamsDict['anisotropy_texture'])                
                anisoTexNode.image = img

                output = anisoTexNode.outputs[0]
                input = groupNode.inputs['anisotropy']
                mat.node_tree.links.new(input, output)             

            else:
                pass

            
  

            ### rotation texture

            if cyclesParamsDict['use_rotation_texture'] == 'on':

                rotationTexNode = nodes.new('ShaderNodeTexImage')
                rotationTexNode.name = 'Rotation Texture'
                rotationTexNode.label = 'Rotation Texture'

                img = D.images.load(cyclesParamsDict['rotation_texture'])                
                rotationTexNode.image = img

                output = rotationTexNode.outputs[0]
                input = groupNode.inputs['rotation']
                mat.node_tree.links.new(input, output)                    
                      
            else:
                pass

            groupNode.inputs["roughness"].default_value = float(cyclesParamsDict['roughness'])
            groupNode.inputs["diffuseColor"].default_value = (float(cyclesParamsDict['diffuse_colorr']),float(cyclesParamsDict['diffuse_colorg']), float(cyclesParamsDict['diffuse_colorb']),1.0)
            groupNode.inputs["glossyColor"].default_value = (float(cyclesParamsDict['glossy_colorr']),float(cyclesParamsDict['glossy_colorg']), float(cyclesParamsDict['glossy_colorb']),1.0)
            groupNode.inputs["fresnelMult"].default_value = float(cyclesParamsDict['fresnel_mult'])



      

            if cyclesParamsDict['use_point_color'] == 'on':
                groupNode.inputs['vertexColorMult'].default_value = 1.0
            else:
                groupNode.inputs['vertexColorMult'].default_value = 0.0

       


            dispTexNode = nodes.new('ShaderNodeTexImage')
            dispTexNode.name = 'Displacement Texture'
            dispTexNode.label = 'Displacement Texture'
            if cyclesParamsDict['use_displacement'] == 'on':

                img = D.images.load(cyclesParamsDict['displacement_texture'])
                groupNode.inputs['displacementAmount'].default_value = float(cyclesParamsDict['displacement_amount'])
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

                if cyclesParamsDict['use_diffuse_texture_alpha'] == 'on':
                    output = diffTexNode.outputs['Alpha']
                    input = groupNode.inputs['alpha']
                    mat.node_tree.links.new(input,output)
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
            groupNode.inputs["diffuseColor"].default_value = (float(cyclesParamsDict['diffuse_colorr']),float(cyclesParamsDict['diffuse_colorg']), float(cyclesParamsDict['diffuse_colorb']),1.0)
            groupNode.inputs["glossyColor"].default_value = (float(cyclesParamsDict['glossy_colorr']),float(cyclesParamsDict['glossy_colorg']), float(cyclesParamsDict['glossy_colorb']),1.0)
            groupNode.inputs["translucentColor"].default_value = (float(cyclesParamsDict['translucent_colorr']),float(cyclesParamsDict['translucent_colorg']), float(cyclesParamsDict['translucent_colorb']),1.0)
            groupNode.inputs["fresnelMult"].default_value = float(cyclesParamsDict['fresnel_mult'])


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
                groupNode.inputs['displacementAmount'].default_value = float(cyclesParamsDict['displacement_amount'])
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


        return mat



    	


if __name__ == "__main__":
        x = createBlendFile()
        bpy.ops.wm.save_mainfile(filepath= fbxFilePath[:-4]+'.blend')
        print("create blend file", bpy)
        print ('{gui2one_INFOS:} --->',' DONE', 'isLast -->', isLast)  


bpy.ops.wm.quit_blender()
