import bpy
C = bpy.context
D = bpy.data

print(D)

for mat in D.materials:
    if mat.users == 0:
        D.materials.remove(mat)

mats = D.materials

newMat = D.materials.new(name='glossy_diffuse')
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