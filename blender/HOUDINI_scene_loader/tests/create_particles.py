import bpy

mesh = bpy.data.meshes.new('mesh')
object = bpy.data.objects.new('test',mesh)

bpy.context.scene.objects.link(object)
bpy.context.scene.objects.active = object

bpy.ops.object.particle_system_add()
active = bpy.context.active_object

settings = active.particle_systems[0].settings
cache = active.particle_systems[0].point_cache

settings.frame_start = 20
settings.count = 150

cache.use_external = True
cache.filepath = 'F:/HOUDINI_15_playground/geo/houdini_cache/'
cache.index = 0
cache.name = 'houdini_cache'

settings.render_type = 'OBJECT'
settings.dupli_object = bpy.data.objects['Torus']
