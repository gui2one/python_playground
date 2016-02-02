import bpy
import mathutils
import math

xAng = bpy.data.objects['Sun'].rotation_euler[0]
yAng = bpy.data.objects['Sun'].rotation_euler[1]
zAng = bpy.data.objects['Sun'].rotation_euler[2]

vec = mathutils.Vector((0.0, 0.0, 1.0))

xMat = mathutils.Matrix( ( ( 1.0, 0.0, 0.0) , (0.0, math.cos(xAng), -math.sin(xAng)), ( 0.0, math.sin(xAng), math.cos(xAng)) ))

yMat = mathutils.Matrix( ( (math.cos(yAng), 0.0, math.sin(yAng)), (0.0, 1.0, 0.0), (-math.sin(yAng), 0.0, math.cos(yAng)) ))

zMat = mathutils.Matrix( ( (math.cos(zAng), -math.sin(zAng), 0.0), (math.sin(zAng), math.cos(zAng),0.0), (0.0, 0.0, 1.0) ))


vec = xMat * vec
vec = yMat * vec
vec = zMat * vec

bpy.data.worlds['World'].node_tree.nodes['Sky Texture'].sun_direction = vec
print (zMat)