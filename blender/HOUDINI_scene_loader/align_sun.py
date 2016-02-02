import bpy
import mathutils
import math

sunLamp = bpy.data.objects['Sun']

lampEuler = mathutils.Euler(sunLamp.rotation_euler, sunLamp.rotation_mode)

sunVec = mathutils.Vector((0.0,0.0,1.0))
sunVec.rotate(lampEuler)



bpy.data.worlds['World'].node_tree.nodes['Sky Texture'].sun_direction = sunVec
