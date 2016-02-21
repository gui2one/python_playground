import bpy
import math
import os
import sys
import xml.dom.minidom as dom
from bpy.app.handlers import persistent
import math




class HoudiniSceneLoaderOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.houdini_scene_loader_operator"
    bl_label = "Load Houdini Scene"
    bl_context = "scene"

    

    def initData(self):  
        print('gui2one_INFOS:loading_started')
        pass  
    
            
    def printInfos(self):
        print('infos !!!!')
    
    def loadShaders(self):
        D = bpy.data
        C = bpy.context

        PYTHON_PLAYGROUND = os.getenv('PYTHON_PLAYGROUND')
        if not PYTHON_PLAYGROUND:
            print('ERROR : PYTHON_PLAYGROUND env variables NOT set')
            sys.exit(0)
        filepath = PYTHON_PLAYGROUND+"/blender/HOUDINI_scene_loader/shaders/shaders_01.blend"
        # shaderName = "diffuseGlossyCustomShader"
        shaderName = ["diffuseGlossyCustomShader","diffuseGlossyTranslucentCustomShader","diffuseAnisotropicCustomShader","emissionCustomShader","glassCustomShader","volumeCustomShader","diffuseGlossySSSCustomShader"]
        # append, set to true to keep the link to the original file
        link = False 



        # append all groups from the .blend file

        with bpy.data.libraries.load(filepath, link=link) as (data_src, data_dst):

            # print('hey', dir(data_src.objects[0]))
            # print('ho', data_src.materials[0])
            
            data_dst.node_groups = shaderName
            
            # bpy.data.node_groups.new(shaderName, 'ShaderNodeTree')

    def createShaders_V3(self, xmlFile):

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
        materialList = xmlData.firstChild.getElementsByTagName('materials')[0]
        doMatteShading = xmlData.firstChild.getElementsByTagName('sceneOptions')[0].getAttribute('volumePass') == 'True'
        for material in materialList.getElementsByTagName('material'):
            materialName = material.getAttribute('name')
            cyclesParamsDict = {}
            for child in material.childNodes:
                if child.nodeType == 1:
                    cyclesParamsDict[child.nodeName] = child.getAttribute('value')

            print ('---------------------------')
            print (cyclesParamsDict)    

            self.initShader(materialName,cyclesParamsDict['shader_type'], cyclesParamsDict, doMatteShading )     

            # print (material.getAttribute('name'),  "--->", material.childNodes)
        

        ## now, good materials were created, but they still don't have the right name ( e.g they have '.001' at the end)

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


    def initBackground(self, xmlFile):
        scene = bpy.data.scenes['Scene']
        scene.world.use_nodes = True


        xmlData = dom.parse(xmlFile)
        background = xmlData.firstChild.getElementsByTagName('background')[0]

        bgType = background.getAttribute('type')
        bgNodes = scene.world.node_tree.nodes
        nodeTree = scene.world.node_tree

        bgNodes['Background'].inputs[1].default_value = float( background.getAttribute('strength'))
        if bgType == 'Color':
            bgNodes['Background'].inputs[0].default_value = ( float(background.getAttribute('BackgroundColorr')) ,
                                                           float(background.getAttribute('BackgroundColorg')) ,
                                                           float(background.getAttribute('BackgroundColorb')), 
                                                           1.0)
        elif bgType == 'Sky':
            skyNode = bgNodes.new(type='ShaderNodeTexSky')
            skyNode.turbidity = float( background.getAttribute('SkyTurbidity'))

            if background.getAttribute('SkyType') == 'Hosek/Wilkie':
                skyNode.sky_type = 'HOSEK_WILKIE'
                skyNode.ground_albedo = float( background.getAttribute('GroundAlbedo'))
            input = skyNode.outputs[0]
            output = bgNodes['Background'].inputs[0]
            nodeTree.links.new(input,output)

            skyNode.sun_direction = ( float(background.getAttribute('SunDirectionx')),
                                      float(background.getAttribute('SunDirectiony')),
                                      float(background.getAttribute('SunDirectionz')))
            # combineNode = bgNodes.new(type='ShaderNodeCombineXYZ')

            # valueXNode = bgNodes.new(type='ShaderNodeValue')
            # valueXNode.outputs[0].default_value = float( background.getAttribute('SunDirectionx'))
            # nodeTree.links.new( valueXNode.outputs[0] , combineNode.inputs[0])

            # valueYNode = bgNodes.new(type='ShaderNodeValue')
            # valueYNode.outputs[0].default_value = float( background.getAttribute('SunDirectiony'))
            # nodeTree.links.new( valueYNode.outputs[0] , combineNode.inputs[1])

            # valueZNode = bgNodes.new(type='ShaderNodeValue')
            # valueZNode.outputs[0].default_value = float( background.getAttribute('SunDirectionz'))
            # nodeTree.links.new( valueZNode.outputs[0] , combineNode.inputs[2])


            # nodeTree.links.new( combineNode.outputs[0], skyNode.inputs['Vector'])



    def initShader(self, objName , shaderType, cyclesParamsDict, doMatteShading):

        D = bpy.data
        C = bpy.context

        

        mat = D.materials.new(objName)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        # if len(D.objects[objName].data.materials) == 0:
        #     D.objects[objName].data.materials.append(mat)
        # else :
        #     D.objects[objName].data.materials[0] = mat


        if shaderType == 'volume':


            shaderName = "volumeCustomShader"
            groupNode = nodes.new('ShaderNodeGroup')
            groupNode.node_tree = bpy.data.node_groups[shaderName]   

                
   

            nodeToDelete = nodes['Diffuse BSDF']
            nodes.remove(nodeToDelete)


            ## set emission color to diffuse color
            groupNode.inputs['scatterColor'].default_value = (float(cyclesParamsDict['scatter_colorr']),float(cyclesParamsDict['scatter_colorg']), float(cyclesParamsDict['scatter_colorb']),1.0)
            groupNode.inputs['scatterDensity'].default_value = float(cyclesParamsDict['scatter_density'])
            groupNode.inputs['absorptionColor'].default_value = (float(cyclesParamsDict['absorption_colorr']),float(cyclesParamsDict['absorption_colorg']), float(cyclesParamsDict['absorption_colorb']),1.0)
            groupNode.inputs['absorptionDensity'].default_value = float(cyclesParamsDict['absorption_density'])
            
            outputNode = nodes['Material Output']
            output = groupNode.outputs['Volume']
            input = outputNode.inputs[1]
            mat.node_tree.links.new(input, output)    

        elif shaderType == 'emission':


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


            #############
            #####   MATTE SHADING
            #############
            if doMatteShading:
                groupNode.inputs['diffColorMult'] .default_value = 0.0
                groupNode.inputs['glossyColorMult'] .default_value = 0.0
                groupNode.inputs['diffTextureMult'] .default_value = 0.0
                groupNode.inputs['vertexColorMult'] .default_value = 0.0

        elif shaderType == 'glass':


            shaderName = "glassCustomShader"
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


            #############
            #####   MATTE SHADING
            #############
            if doMatteShading:
                groupNode.inputs['diffColorMult'] .default_value = 0.0
                groupNode.inputs['glossyColorMult'] .default_value = 0.0
                groupNode.inputs['diffTextureMult'] .default_value = 0.0
                groupNode.inputs['vertexColorMult'] .default_value = 0.0

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

            #############
            #####   MATTE SHADING
            #############
            if doMatteShading:
                groupNode.inputs['diffColorMult'] .default_value = 0.0
                groupNode.inputs['glossyColorMult'] .default_value = 0.0
                groupNode.inputs['diffTextureMult'] .default_value = 0.0
                groupNode.inputs['vertexColorMult'] .default_value = 0.0             
                groupNode.inputs['translucentColorMult'] .default_value = 0.0             
                groupNode.inputs['translucentTextureMult'] .default_value = 0.0  

        elif shaderType == 'diffuse+glossy+SSS':


            shaderName = "diffuseGlossySSSCustomShader"
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

            groupNode.inputs["fresnelMult"].default_value = float(cyclesParamsDict['fresnel_mult'])
            groupNode.inputs["SSSColor"].default_value = (float(cyclesParamsDict['sss_colorr']),float(cyclesParamsDict['sss_colorg']), float(cyclesParamsDict['sss_colorb']),1.0)            
            groupNode.inputs["SSSScale"].default_value = float(cyclesParamsDict['sss_scale'])
            groupNode.inputs["SSSRadius"].default_value = (float(cyclesParamsDict['sss_radiusx']),float(cyclesParamsDict['sss_radiusy']), float(cyclesParamsDict['sss_radiusz']))            


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

            #############
            #####   MATTE SHADING
            #############
            if doMatteShading:
                groupNode.inputs['diffColorMult'] .default_value = 0.0
                groupNode.inputs['glossyColorMult'] .default_value = 0.0
                groupNode.inputs['diffTextureMult'] .default_value = 0.0
                groupNode.inputs['vertexColorMult'] .default_value = 0.0             
                groupNode.inputs['translucentColorMult'] .default_value = 0.0             
                groupNode.inputs['translucentTextureMult'] .default_value = 0.0  
        return mat

    
    def loadXMLData(self, xmlFile):
        # print('loadXMLData function -------')
        confPath = bpy.context.scene.conf_path
        projectDir = os.path.split(confPath)[0]

        xmlData = dom.parse(xmlFile)
        camList = xmlData.firstChild.getElementsByTagName('camera')
        objList = xmlData.firstChild.getElementsByTagName('object')
        lightList = xmlData.firstChild.getElementsByTagName('light')
        instanceList = xmlData.firstChild.getElementsByTagName('instance')



        ### import INSTANCES
        instanceListStipped = []
        for instance in instanceList:
            name = instance.getAttribute('sourceObjectName')
            if name not in instanceListStipped:
                instanceListStipped.append(name)

        for sourceObjectName in instanceListStipped:
            path = '%s/geo/%s.blend'  % (projectDir, sourceObjectName)
            print ('{INFOS} ------------>',path)
            ### link instance

            
            sourceObjectPath = '%s/geo/%s.blend'  % (projectDir, sourceObjectName)

            objToLink = [sourceObjectName]
            # append, set to true to keep the link to the original file
            link = False 



            # append all groups from the .blend file

            with bpy.data.libraries.load(sourceObjectPath, link=link) as (data_src, data_dst):

                # print('hey', dir(data_src.objects[0]))
                # print('ho', data_src.materials[0])
                
                data_dst.objects = objToLink

            # print('{INFOS} --> |||000', data_dst.objects)

            #link object to current scene

            scn = bpy.context.scene
            for obj in data_dst.objects:
                if obj is not None:
                    scn.objects.link(obj)       


            
            bpy.context.scene.objects.active = bpy.context.scene.objects[sourceObjectName]
            
            ## put the object in a group
            bpy.ops.object.group_add()
            bpy.data.groups['Group'].name = sourceObjectName
            bpy.ops.object.group_link(group=sourceObjectName)      

            bpy.data.objects[sourceObjectName].layers[1] = True
            bpy.data.objects[sourceObjectName].layers[0] = False
        # print('{INFOS} -->', sourceObjectName)
        # print('{INFOS} -->', sourceObjectPath)

        for instance in instanceList:
            sourceObjectName = instance.getAttribute('sourceObjectName')
            name = instance.getAttribute('name')
            cyclesParams =  instance.getElementsByTagName('cyclesParams')[0]



            bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0))
            empty = bpy.context.active_object
            bpy.context.object.dupli_type = 'GROUP'
            bpy.context.object.dupli_group = bpy.data.groups[sourceObjectName]

            empty.name = '%s_dummy' % (name)

            transforms = instance.getElementsByTagName('transforms')[0]
            rotation = transforms.getAttribute('rotation').strip('[,]').split(',')
            translation = transforms.getAttribute('translation').strip('[,]').split(',')

            empty.rotation_mode = 'QUATERNION' 
            empty.rotation_quaternion[0] = float(rotation[3]) ##W
            empty.rotation_quaternion[1] = float(rotation[0]) ##X
            empty.rotation_quaternion[2] = float(rotation[1]) ##Y
            empty.rotation_quaternion[3] = float(rotation[2]) ##Z       

            empty.location[0] = float(translation[0])
            empty.location[1] = float(translation[1])
            empty.location[2] = float(translation[2])         

            cyclesParamsDict = {}
            for child in cyclesParams.childNodes:
                if child.nodeType == 1: ######### ???
                    cyclesParamsDict[child.nodeName] = child.getAttribute('value')
            

            empty.cycles_visibility.camera = int(cyclesParamsDict['ray_vis_camera'] == 'on')
            empty.cycles_visibility.diffuse = int(cyclesParamsDict['ray_vis_diffuse'] == 'on')
            empty.cycles_visibility.glossy = int(cyclesParamsDict['ray_vis_glossy'] == 'on')
            empty.cycles_visibility.transmission = int(cyclesParamsDict['ray_vis_transmission'] == 'on')
            empty.cycles_visibility.scatter = int(cyclesParamsDict['ray_vis_volume_scatter'] == 'on')
            empty.cycles_visibility.shadow = int(cyclesParamsDict['ray_vis_shadow'] == 'on')


        

        # imports Lights
        for light in lightList:

            lightName = light.getAttribute('name')
            lightType = light.getAttribute('lightType')
            lightSizeX = light.getAttribute('sizex')
            lightSizeY = light.getAttribute('sizey')
            light_emission_strength = light.getAttribute('emissionStrength')
            light_color  = light.getAttribute('color').split(',')



            try : 
                candidate = bpy.context.scene.objects[lightName]

                bpy.ops.object.select_all(action='DESELECT')
                candidate.select = True
                print (candidate.name, "delete -----------------")
                bpy.ops.object.delete()
                bpy.ops.object.select_all(action='DESELECT')
            except:
                pass                     

            isLightAnimated = light.getAttribute('isAnimated') == 'True'
            
   
            
            ### create light object
            if lightType == 'grid':
                lightLight = bpy.data.lamps.new(lightName,'AREA')
                lightLight.shape = 'RECTANGLE'
                lightLight.size = float(lightSizeX)
                lightLight.size_y = float(lightSizeY)                
            elif lightType == 'sphere':
                lightLight = bpy.data.lamps.new(lightName,'POINT')
                lightLight.shadow_soft_size = float(lightSizeX)


            lightLight.cycles.use_multiple_importance_sampling = True
            lightObj = bpy.data.objects.new(lightName, lightLight)
            bpy.context.scene.objects.link(lightObj)




            lightLight.use_nodes = True
            lightLight.node_tree.nodes['Emission'].inputs['Strength'].default_value = float(light_emission_strength)
            lightLight.node_tree.nodes['Emission'].inputs['Color'].default_value = (float(light_color[0]) , float(light_color[1]), float(light_color[2]),1.0)



            if isLightAnimated:
                transformAnimation = light.getElementsByTagName('transformAnimation')[0]
                frames = transformAnimation.getElementsByTagName('frame')
                for frame in frames:
                    frameNumber= int(frame.getAttribute('frameNumber'))
                    translation = frame.getAttribute('translation').strip('[,]').split(',')
                    rotation = frame.getAttribute('rotation').strip('[,]').split(',')

                    lightObj.rotation_mode = 'QUATERNION'
                    lightObj.rotation_quaternion[0] = float(rotation[3]) ##W
                    lightObj.rotation_quaternion[1] = float(rotation[0]) ##X
                    lightObj.rotation_quaternion[2] = float(rotation[1]) ##Y
                    lightObj.rotation_quaternion[3] = float(rotation[2]) ##Z
                    lightObj.keyframe_insert(data_path='rotation_quaternion', frame=frameNumber)

                    lightObj.location[0] = float(translation[0])
                    lightObj.location[1] = float(translation[1])
                    lightObj.location[2] = float(translation[2])

                    lightObj.keyframe_insert(data_path='location', frame=frameNumber)


            else:
                transforms = light.getElementsByTagName('transforms')[0]
                translation = transforms.getAttribute('translation').strip('[,]').split(',')
                rotation = transforms.getAttribute('rotation').strip('[,]').split(',')

                lightObj.rotation_mode = 'QUATERNION' 
                lightObj.rotation_quaternion[0] = float(rotation[3]) ##W
                lightObj.rotation_quaternion[1] = float(rotation[0]) ##X
                lightObj.rotation_quaternion[2] = float(rotation[1]) ##Y
                lightObj.rotation_quaternion[3] = float(rotation[2]) ##Z       

                lightObj.location[0] = float(translation[0])
                lightObj.location[1] = float(translation[1])
                lightObj.location[2] = float(translation[2])
   
         


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
            isCamAnimated = cam.getAttribute('isAnimated') == 'True'
            




            fbxFilePath = '%s/geo/%s.fbx' % (projectDir,camName)

            ### import FBX camera
            # bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100) 
            # camObj =  bpy.context.scene.objects[camName] 
            # camCam = bpy.data.cameras[camName]                     
            
            ### create camera ( as opposed to import FBX camera )
            camCam = bpy.data.cameras.new(camName)
            camObj = bpy.data.objects.new(camName, camCam)
            bpy.context.scene.objects.link(camObj)


            
            camCam.cycles.aperture_type = "FSTOP"
            camCam.cycles.aperture_fstop = fstop
            
       



            if isCamAnimated:
                transformAnimation = cam.getElementsByTagName('transformAnimation')[0]
                frames = transformAnimation.getElementsByTagName('frame')
                for frame in frames:
                    frameNumber= int(frame.getAttribute('frameNumber'))
                    translation = frame.getAttribute('translation').strip('[,]').split(',')
                    rotation = frame.getAttribute('rotation').strip('[,]').split(',')

                    
                    # camObj.rotation_euler[2] = math.radians(float(rotation[1])*-1)
                    # camObj.rotation_euler[1] = math.radians(float(rotation[2]))
                    # camObj.rotation_euler[0] = math.radians(float(rotation[0])+90.0)
                    # camObj.keyframe_insert(data_path='rotation_euler', frame=frameNumber)
                    camObj.rotation_mode = 'QUATERNION'
                    camObj.rotation_quaternion[0] = float(rotation[3]) ##W
                    camObj.rotation_quaternion[1] = float(rotation[0]) ##X
                    camObj.rotation_quaternion[2] = float(rotation[1]) ##Y
                    camObj.rotation_quaternion[3] = float(rotation[2]) ##Z
                    camObj.keyframe_insert(data_path='rotation_quaternion', frame=frameNumber)

                    camObj.location[0] = float(translation[0])
                    camObj.location[1] = float(translation[1])
                    camObj.location[2] = float(translation[2])

                    camObj.keyframe_insert(data_path='location', frame=frameNumber)
                    # print(float(translation[0]))
                    # print(float(rotation[0]))

            else:
                transforms = cam.getElementsByTagName('transforms')[0]
                translation = transforms.getAttribute('translation').strip('[,]').split(',')
                rotation = transforms.getAttribute('rotation').strip('[,]').split(',')

                camObj.rotation_mode = 'QUATERNION' 
                camObj.rotation_quaternion[0] = float(rotation[3]) ##W
                camObj.rotation_quaternion[1] = float(rotation[0]) ##X
                camObj.rotation_quaternion[2] = float(rotation[1]) ##Y
                camObj.rotation_quaternion[3] = float(rotation[2]) ##Z       

                camObj.location[0] = float(translation[0])
                camObj.location[1] = float(translation[1])
                camObj.location[2] = float(translation[2])
                

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
            animationType = obj.getAttribute('animation_type')
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
            isObjAnim = obj.getAttribute('isObjAnim') == 'True'



  
            ### import fbx
            if animationType == 'mesh_cache' or not isPointAnim:
                fbxFilePath = '%s/geo/%s.fbx' % (projectDir, objName)
                bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, use_image_search=False)
            else:
                # print("load file path current frame")
                fbxFilePath = '%s/geo/%s_sequence/%s_1.fbx' % (projectDir, objName, objName)
                bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, use_image_search=False)
            
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


            if not isObjAnim:
                objTransforms = obj.getElementsByTagName('transforms')[0]
                
                objTranslation = objTransforms.getElementsByTagName('translation')[0].childNodes[0].data.split(' ')
                objRotation = objTransforms.getElementsByTagName('rotation')[0].childNodes[0].data.split(' ')
                objScale = objTransforms.getElementsByTagName('scale')[0].childNodes[0].data.split(' ')

                fbxObj.location[0] = float(objTranslation[0])
                fbxObj.location[1] = float(objTranslation[2])*-1
                fbxObj.location[2] = float(objTranslation[1])
                    # camObj.rotation_euler[2] = math.radians(float(rotation[1])*-1)
                    # camObj.rotation_euler[1] = math.radians(float(rotation[2]))
                    # camObj.rotation_euler[0] = math.radians(float(rotation[0])+90.0)

                fbxObj.rotation_euler[0] = math.radians(float(objRotation[0])+90)
                fbxObj.rotation_euler[1] = math.radians(float(objRotation[2])*-1)
                fbxObj.rotation_euler[2] = math.radians(float(objRotation[1]))

                fbxObj.rotation_mode = 'XZY'

                # fbxObj.rotation_mode = 'QUATERNION' 
                # fbxObj.rotation_quaternion[0] = float(objRotation[3]) ##W
                # fbxObj.rotation_quaternion[1] = float(objRotation[0]) ##X
                # fbxObj.rotation_quaternion[2] = float(objRotation[1]) ##Y
                # fbxObj.rotation_quaternion[3] = float(objRotation[2]) ##Z                       
                
                fbxObj.scale[0] = float(objScale[0])                
                fbxObj.scale[1] = float(objScale[1])      
                fbxObj.scale[2] = float(objScale[2])                          

            fbxObj.cycles_visibility.camera = int(cyclesParamsDict['ray_vis_camera'] == 'on')
            fbxObj.cycles_visibility.diffuse = int(cyclesParamsDict['ray_vis_diffuse'] == 'on')
            fbxObj.cycles_visibility.glossy = int(cyclesParamsDict['ray_vis_glossy'] == 'on')
            fbxObj.cycles_visibility.transmission = int(cyclesParamsDict['ray_vis_transmission'] == 'on')
            fbxObj.cycles_visibility.scatter = int(cyclesParamsDict['ray_vis_volume_scatter'] == 'on')
            fbxObj.cycles_visibility.shadow = int(cyclesParamsDict['ray_vis_shadow'] == 'on')


        fbxObj.rotation_mode = 'XZY'
            
            
      



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
                currentFrameObj = bpy.ops.import_scene.fbx(filepath=fbxFilePath, global_scale=100, use_image_search=False)
                # currentFrameObj.name = objName    
                fbxObj = bpy.context.scene.objects[objName]
                fbxObj.data.use_auto_smooth = False     

                #### materials
                # try:
                #     if len(fbxObj.data.materials) != 0:
                #         fbxObj.data.materials[0] = bpy.data.materials[objName]
                #     else:    
                #         fbxObj.data.materials.append(bpy.data.materials[objName])
                # except:
                #     pass                           
                    
        bpy.app.handlers.frame_change_pre.append(callbackFunction )
        # bpy.app.handlers.render_pre.append(callbackFunction )


    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        # self.report({'INFO'}, "Loading Houdini XML custom Scene File")
        xmlFile = bpy.context.scene.conf_path

        self.initData()
        self.printInfos()
        self.loadShaders()
        self.loadXMLData(xmlFile)
        self.createShaders_V3(xmlFile)
        self.initBackground(xmlFile)

        print('gui2one_INFOS:loading_finished')
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